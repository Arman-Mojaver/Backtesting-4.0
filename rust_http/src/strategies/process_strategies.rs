use crate::strategies::operation_points_map::get_operation_points_map;
use crate::strategies::process_strategy::get_process_strategy;
use crate::strategies::{OperationPoint, SignalGroup, Strategy};
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Serialize, Deserialize)]
pub struct ProcessStrategiesPayload {
    money_management_strategy_id: u32,
    operation_points: OperationPoints,
    signal_groups: HashMap<u32, SignalGroup>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct OperationPoints {
    long_operation_points: Vec<OperationPoint>,
    short_operation_points: Vec<OperationPoint>,
}

pub async fn process_strategies(payload: web::Json<ProcessStrategiesPayload>) -> impl Responder {
    let strategies = get_process_strategies(
        &payload.operation_points,
        payload.money_management_strategy_id,
        &payload.signal_groups,
    );
    HttpResponse::Ok().json(serde_json::json!({ "data": strategies }))
}

pub fn get_process_strategies(
    operation_points: &OperationPoints,
    money_management_strategy_id: u32,
    signal_groups: &HashMap<u32, SignalGroup>,
) -> Vec<Strategy> {
    let mut strategies = Vec::new();
    let long_operation_points = operation_points.long_operation_points.clone();
    let long_operation_points_map = get_operation_points_map(long_operation_points);

    let short_operation_points = operation_points.short_operation_points.clone();
    let short_operation_points_map = get_operation_points_map(short_operation_points);

    let timestamps: Vec<u32> = operation_points
        .long_operation_points
        .iter()
        .map(|op| op.timestamp)
        .collect();

    let start_date = *timestamps.iter().min().unwrap();
    let end_date = *timestamps.iter().max().unwrap();

    let mut indicator_ids: Vec<&u32> = signal_groups.keys().collect();
    indicator_ids.sort();

    for indicator_id in indicator_ids {
        let signal_group = signal_groups.get(indicator_id).unwrap();

        let strategy = get_process_strategy(
            &long_operation_points_map,
            &short_operation_points_map,
            signal_group,
            start_date,
            end_date,
            money_management_strategy_id,
            *indicator_id,
        );

        strategies.push(strategy);
    }

    strategies
}
