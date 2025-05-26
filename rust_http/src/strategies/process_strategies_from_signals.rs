use crate::strategies::operation_points_table::get_operation_points_table;
use crate::strategies::process_strategy::{get_process_strategy, StrategyGroup};
use crate::strategies::{OperationPoint, SignalGroup};
use actix_web::{web, HttpResponse, Responder};
use crossbeam::channel;
use log::info;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use std::thread;
use std::time::Instant;

#[derive(Debug, Serialize, Deserialize)]
pub struct ProcessStrategiesFromSignalsPayload {
    money_management_strategy_id: i32,
    long_operation_points: Vec<OperationPoint>,
    short_operation_points: Vec<OperationPoint>,
    signal_groups: HashMap<i32, SignalGroup>,
}

pub async fn process_strategies_from_signals(
    payload: web::Json<ProcessStrategiesFromSignalsPayload>,
) -> impl Responder {
    let strategy_groups = get_process_strategies_from_signals(
        &payload.long_operation_points,
        &payload.short_operation_points,
        payload.money_management_strategy_id,
        &payload.signal_groups,
    );
    HttpResponse::Ok().json(serde_json::json!({ "data": strategy_groups }))
}

#[derive(Debug)]
struct ProcessTask {
    signal_group: SignalGroup,
    start_date: i32,
    end_date: i32,
    money_management_strategy_id: i32,
    indicator_id: i32,
}

pub fn get_process_strategies_from_signals(
    long_operation_points: &Vec<OperationPoint>,
    short_operation_points: &Vec<OperationPoint>,
    money_management_strategy_id: i32,
    signal_groups: &HashMap<i32, SignalGroup>,
) -> Vec<StrategyGroup> {
    let start = Instant::now();
    info!("/process_strategies_from_signals. Starting");

    let mut strategy_groups = Vec::new();
    let long_operation_points_table = get_operation_points_table(long_operation_points);
    let short_operation_points_table = get_operation_points_table(short_operation_points);

    let timestamps: Vec<i32> = long_operation_points
        .iter()
        .map(|op| op.timestamp)
        .collect();

    let start_date = *timestamps.iter().min().unwrap();
    let end_date = *timestamps.iter().max().unwrap();

    let mut indicator_ids: Vec<&i32> = signal_groups.keys().collect();
    indicator_ids.sort();

    let (work_sender, work_receiver) = channel::unbounded::<ProcessTask>();
    let (result_sender, result_receiver) = channel::unbounded::<StrategyGroup>();

    let mut handles = Vec::new();
    for _ in 0..7 {
        let long_table = Arc::clone(&long_operation_points_table);
        let short_table = Arc::clone(&short_operation_points_table);
        let work_rx = work_receiver.clone();
        let result_tx = result_sender.clone();

        let handle = thread::spawn(move || {
            while let Ok(task) = work_rx.recv() {
                let strategy = get_process_strategy(
                    &long_table,
                    &short_table,
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
                signal_group,
                start_date,
                end_date,
                money_management_strategy_id,
                indicator_id: *indicator_id,
            })
            .unwrap();
    }

    drop(work_sender);
    drop(result_sender);

    for strategy_group in result_receiver.iter() {
        strategy_groups.push(strategy_group);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    strategy_groups.sort_by_key(|s| s.strategy.indicator_id);

    let total_elapsed = start.elapsed();
    info!("Process time: {:?}", total_elapsed);

    strategy_groups
}
