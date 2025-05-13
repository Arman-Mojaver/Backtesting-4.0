use crate::strategies::annual_operation_count::get_annual_operation_count;
use crate::strategies::annual_roi_from_global_roi::get_annual_roi_from_global_roi;
use crate::strategies::global_roi::get_global_roi;
use crate::strategies::max_draw_down::get_max_draw_down;
use crate::strategies::operation_points_filter::get_operation_points_filter;
use crate::strategies::{OperationPoint, SignalGroup, Strategy};
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use rustc_hash::FxHashMap;

#[derive(Debug, Serialize, Deserialize)]
pub struct ProcessStrategyPayload {
    long_operation_points_map: FxHashMap<u32, OperationPoint>,
    short_operation_points_map: FxHashMap<u32, OperationPoint>,
    signal_group: SignalGroup,
    start_date: u32,
    end_date: u32,
    money_management_strategy_id: u32,
    indicator_id: u32,
}

pub async fn process_strategy(payload: web::Json<ProcessStrategyPayload>) -> impl Responder {
    let long_operation_points_map: FxHashMap<u32, &OperationPoint> = payload
        .long_operation_points_map
        .iter()
        .map(|(&k, v)| (k, v))
        .collect();
    let short_operation_points_map: FxHashMap<u32, &OperationPoint> = payload
        .short_operation_points_map
        .iter()
        .map(|(&k, v)| (k, v))
        .collect();

    let strategy = get_process_strategy(
        &long_operation_points_map,
        &short_operation_points_map,
        &payload.signal_group,
        payload.start_date,
        payload.end_date,
        payload.money_management_strategy_id,
        payload.indicator_id,
    );

    HttpResponse::Ok().json(serde_json::json!({ "data": strategy }))
}

pub fn get_process_strategy(
    long_operation_points_map: &FxHashMap<u32, &OperationPoint>,
    short_operation_points_map: &FxHashMap<u32, &OperationPoint>,
    signal_group: &SignalGroup,
    start_date: u32,
    end_date: u32,
    money_management_strategy_id: u32,
    indicator_id: u32,
) -> Strategy {
    let operation_point_list = get_operation_points_filter(
        long_operation_points_map,
        short_operation_points_map,
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
