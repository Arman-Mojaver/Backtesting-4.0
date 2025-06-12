use crate::strategies::operation_points_table::get_operation_points_table;
use crate::strategies::process_strategy::{get_process_strategy, StrategyGroup};
use crate::strategies::{OperationPoint, SignalGroup};
use actix_web::{web, HttpResponse, Responder};
use log::info;
use rayon::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use std::time::Instant;

#[derive(Debug, Serialize, Deserialize)]
pub struct ProcessStrategiesFromSignalsPayload {
    instrument: String,
    money_management_strategy_id: i32,
    long_operation_points: Vec<OperationPoint>,
    short_operation_points: Vec<OperationPoint>,
    signal_groups: HashMap<i32, SignalGroup>,
}

pub async fn process_strategies_from_signals(
    payload: web::Json<ProcessStrategiesFromSignalsPayload>,
) -> impl Responder {
    let strategy_groups = get_process_strategies_from_signals(
        payload.instrument.clone(),
        &payload.long_operation_points,
        &payload.short_operation_points,
        payload.money_management_strategy_id,
        &payload.signal_groups,
    );
    HttpResponse::Ok().json(serde_json::json!({ "data": strategy_groups }))
}

pub fn get_process_strategies_from_signals(
    instrument: String,
    long_operation_points: &Vec<OperationPoint>,
    short_operation_points: &Vec<OperationPoint>,
    money_management_strategy_id: i32,
    signal_groups: &HashMap<i32, SignalGroup>,
) -> Vec<StrategyGroup> {
    let start = Instant::now();
    info!("/process_strategies_from_signals. Starting");

    let long_table = Arc::new(get_operation_points_table(long_operation_points));
    let short_table = Arc::new(get_operation_points_table(short_operation_points));

    let timestamps: Vec<i32> = long_operation_points
        .iter()
        .map(|op| op.timestamp)
        .collect();
    let start_date = *timestamps.iter().min().unwrap();
    let end_date = *timestamps.iter().max().unwrap();

    let mut sorted_ids: Vec<i32> = signal_groups.keys().copied().collect();
    sorted_ids.sort_unstable();

    let mut strategy_groups: Vec<StrategyGroup> = sorted_ids
        .into_par_iter()
        .map(|indicator_id| {
            let signal_group = signal_groups.get(&indicator_id).unwrap();
            get_process_strategy(
                instrument.clone(),
                &long_table,
                &short_table,
                signal_group,
                start_date,
                end_date,
                money_management_strategy_id,
                indicator_id,
            )
        })
        .collect();

    let total_elapsed = start.elapsed();
    info!("Process time: {:?}", total_elapsed);

    strategy_groups
}
