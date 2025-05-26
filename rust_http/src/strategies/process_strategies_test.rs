use crate::config::DbConfig;
use crate::db::init_pool;
use crate::strategies::process_strategies::get_process_strategies;
use crate::strategies::query_indicators::get_query_indicators;
use crate::strategies::query_long_operation_points::get_query_long_operation_points;
use crate::strategies::query_resampled_points::get_query_resampled_points;
use crate::strategies::query_short_operation_points::get_query_short_operation_points;
use actix_web::{web, HttpResponse, Responder};
use log::info;
use serde::{Deserialize, Serialize};
use std::time::Instant;

#[derive(Debug, Serialize, Deserialize)]
pub struct ProcessMoneyManagementStrategyPayload {
    instrument: String,
    money_management_strategy_id: i32,
    indicator_type: String,
}

pub async fn process_strategies_test(
    payload: web::Json<ProcessMoneyManagementStrategyPayload>,
) -> impl Responder {
    let start = Instant::now();
    info!("/process_strategies. Starting");

    let db_config = DbConfig::testing();
    let db_pool = init_pool(db_config).await.expect("DB pool init failed");

    let resampled_points = get_query_resampled_points(&db_pool, &payload.instrument).await;
    let indicators = get_query_indicators(&db_pool, &payload.indicator_type).await;
    let long_operation_points =
        get_query_long_operation_points(&db_pool, payload.money_management_strategy_id).await;
    let short_operation_points =
        get_query_short_operation_points(&db_pool, payload.money_management_strategy_id).await;

    let _strategies = get_process_strategies(
        payload.money_management_strategy_id,
        &resampled_points,
        &indicators,
        &long_operation_points,
        &short_operation_points,
    );

    let total_elapsed = start.elapsed();
    info!("Process time (/process_strategies): {:?}", total_elapsed);

    HttpResponse::Ok().json(serde_json::json!({ "data": [] }))
}
