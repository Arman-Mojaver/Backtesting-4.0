use crate::config::DbConfig;
use crate::db::init_pool;
use crate::signals::indicator_types::IndicatorType;
use crate::strategies::process_strategies_from_signals::get_process_strategies_from_signals;
use crate::strategies::process_strategies_validator::get_process_strategies_validator;
use crate::strategies::query_indicators::get_query_indicators;
use crate::strategies::query_long_operation_points::get_query_long_operation_points;
use crate::strategies::query_resampled_points::get_query_resampled_points;
use crate::strategies::query_short_operation_points::get_query_short_operation_points;
use crate::strategies::{Indicator, OperationPoint, ResampledPointD1, SignalGroup};
use actix_web::{web, HttpResponse, Responder};
use log::info;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::str::FromStr;
use std::time::Instant;

#[derive(Debug, Serialize, Deserialize)]
pub struct ProcessStrategiesPayload {
    instrument: String,
    money_management_strategy_id: i32,
    indicator_type: String,
}

pub async fn process_strategies(payload: web::Json<ProcessStrategiesPayload>) -> impl Responder {
    let start = Instant::now();
    info!("/process_strategies. Starting");

    let db_config = DbConfig::from_env();
    let db_pool = init_pool(db_config).await.expect("DB pool init failed");

    let resampled_points = get_query_resampled_points(&db_pool, &payload.instrument).await;
    let indicators = get_query_indicators(&db_pool, &payload.indicator_type).await;
    let long_operation_points =
        get_query_long_operation_points(&db_pool, payload.money_management_strategy_id).await;
    let short_operation_points =
        get_query_short_operation_points(&db_pool, payload.money_management_strategy_id).await;

    match get_process_strategies_validator(
        &long_operation_points,
        &short_operation_points,
        payload.money_management_strategy_id,
        &indicators,
        &resampled_points,
    ) {
        Ok(()) => {}
        Err(e) => panic!("Validation failed: {:?}", e),
    }

    let signal_groups = get_signal_groups(resampled_points, &indicators);

    let total_elapsed = start.elapsed();
    info!("Process time (signal_groups): {:?}", total_elapsed);

    let strategy_groups = get_process_strategies_from_signals(
        payload.instrument.clone(),
        &long_operation_points,
        &short_operation_points,
        payload.money_management_strategy_id,
        &signal_groups,
    );

    let total_elapsed2 = start.elapsed();
    info!("Process time (/process_strategies): {:?}", total_elapsed2);

    HttpResponse::Ok().json(serde_json::json!({ "data": strategy_groups }))
}

fn get_signal_groups(
    resampled_points: Vec<ResampledPointD1>,
    indicators: &Vec<Indicator>,
) -> HashMap<i32, SignalGroup> {
    let mut signal_groups: HashMap<i32, SignalGroup> = HashMap::with_capacity(indicators.len());
    for indicator in indicators {
        let indicator_type: IndicatorType = IndicatorType::from_str(&indicator.r#type).unwrap();
        let indicator_values =
            indicator_type.generate_indicator_values(&resampled_points, &indicator.parameters);
        let signal_group = indicator_values.generate_signals();
        signal_groups.insert(indicator.id, signal_group);
    }
    signal_groups
}

pub fn get_process_strategies(
    _money_management_strategy_id: i32,
    _resampled_points: &Vec<ResampledPointD1>,
    _indicators: &Vec<Indicator>,
    _long_operation_points: &Vec<OperationPoint>,
    _short_operation_points: &Vec<OperationPoint>,
) -> i32 {
    0
}
