use crate::strategies::operation_points_map::get_operation_points_map;
use crate::strategies::process_strategy::get_process_strategy;
use crate::strategies::{OperationPoint, SignalGroup, Strategy};
use actix_web::{web, HttpResponse, Responder};
use crossbeam::channel;
use log::info;
use rustc_hash::FxHashMap;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::thread;
use std::time::Instant;

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

#[derive(Debug)]
struct ProcessTask {
    signal_group: SignalGroup,
    start_date: u32,
    end_date: u32,
    money_management_strategy_id: u32,
    indicator_id: u32,
}

pub fn get_process_strategies(
    operation_points: &OperationPoints,
    money_management_strategy_id: u32,
    signal_groups: &HashMap<u32, SignalGroup>,
) -> Vec<Strategy> {
    let start = Instant::now();
    info!("/process_strategies. Starting");

    let mut strategies = Vec::new();
    let long_operation_points = &operation_points.long_operation_points;
    let long_operation_points_map = get_operation_points_map(long_operation_points);

    let short_operation_points = &operation_points.short_operation_points;
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

    let (work_sender, work_receiver) = channel::unbounded::<ProcessTask>();
    let (result_sender, result_receiver) = channel::unbounded::<Strategy>();

    let mut handles = Vec::new();
    for _ in 0..7 {
        let long_map = long_operation_points_map.clone();
        let short_map = short_operation_points_map.clone();
        let work_rx = work_receiver.clone();
        let result_tx = result_sender.clone();

        let handle = thread::spawn(move || {
            while let Ok(task) = work_rx.recv() {
                let long_ref: FxHashMap<u32, &OperationPoint> =
                    long_map.iter().map(|(&ts, op)| (ts, op)).collect();
                let short_ref: FxHashMap<u32, &OperationPoint> =
                    short_map.iter().map(|(&ts, op)| (ts, op)).collect();

                let strategy = get_process_strategy(
                    &long_ref,
                    &short_ref,
                    &task.signal_group,
                    task.start_date,
                    task.end_date,
                    task.money_management_strategy_id,
                    task.indicator_id,
                );

                result_tx.send(strategy).unwrap();
            }
        });

        handles.push(handle);
    }

    for indicator_id in indicator_ids {
        let signal_group = signal_groups.get(&indicator_id).unwrap().clone();

        work_sender
            .send(ProcessTask {
                signal_group: signal_group,
                start_date: start_date,
                end_date: end_date,
                money_management_strategy_id: money_management_strategy_id,
                indicator_id: *indicator_id,
            })
            .unwrap();
    }

    drop(work_sender);
    drop(result_sender);

    for strategy in result_receiver.iter() {
        strategies.push(strategy);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    strategies.sort_by_key(|s| s.indicator_id);

    let total_elapsed = start.elapsed();
    info!("Process time: {:?}", total_elapsed);

    strategies
}
