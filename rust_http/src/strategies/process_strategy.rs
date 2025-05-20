use crate::strategies::annual_operation_count::get_annual_operation_count;
use crate::strategies::annual_roi_from_global_roi::get_annual_roi_from_global_roi;
use crate::strategies::global_roi::get_global_roi;
use crate::strategies::max_draw_down::get_max_draw_down;
use crate::strategies::operation_points_filter::get_operation_points_filter;
use crate::strategies::{OperationPoint, SignalGroup, Strategy};
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use std::sync::Arc;

#[derive(Debug, Serialize, Deserialize)]
pub struct ProcessStrategyPayload {
    long_operation_points_table: Vec<(i32, OperationPoint)>,
    short_operation_points_table: Vec<(i32, OperationPoint)>,
    signal_group: SignalGroup,
    start_date: i32,
    end_date: i32,
    money_management_strategy_id: i32,
    indicator_id: i32,
}

pub async fn process_strategy(payload: web::Json<ProcessStrategyPayload>) -> impl Responder {
    let payload = payload.into_inner();

    let long_table: Vec<(i32, Arc<OperationPoint>)> = payload
        .long_operation_points_table
        .into_iter()
        .map(|(ts, op)| (ts, Arc::new(op)))
        .collect();

    let short_table: Vec<(i32, Arc<OperationPoint>)> = payload
        .short_operation_points_table
        .into_iter()
        .map(|(ts, op)| (ts, Arc::new(op)))
        .collect();

    let strategy = get_process_strategy(
        &long_table,
        &short_table,
        &payload.signal_group,
        payload.start_date,
        payload.end_date,
        payload.money_management_strategy_id,
        payload.indicator_id,
    );

    HttpResponse::Ok().json(serde_json::json!({ "data": strategy }))
}

pub fn get_process_strategy(
    long_operation_points_table: &Vec<(i32, Arc<OperationPoint>)>,
    short_operation_points_table: &Vec<(i32, Arc<OperationPoint>)>,
    signal_group: &SignalGroup,
    start_date: i32,
    end_date: i32,
    money_management_strategy_id: i32,
    indicator_id: i32,
) -> Strategy {
    let operation_point_list = get_operation_points_filter(
        long_operation_points_table,
        short_operation_points_table,
        signal_group,
    );

    let annual_roi =
        get_annual_roi_from_global_roi(get_global_roi(&operation_point_list), start_date, end_date);
    let max_draw_down = get_max_draw_down(&operation_point_list);
    let annual_operation_count =
        get_annual_operation_count(&operation_point_list, start_date, end_date);

    Strategy {
        annual_roi,
        max_draw_down,
        annual_operation_count,
        money_management_strategy_id,
        indicator_id,
    }
}
