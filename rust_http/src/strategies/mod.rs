pub mod annual_operation_count;
pub mod annual_roi_from_global_roi;
pub mod global_roi;
pub mod max_draw_down;
pub mod operation_points_filter;
pub mod operation_points_map;
pub mod process_strategies;
pub mod process_strategy;

use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct OperationPointsWithDatesPayload {
    operation_points: Vec<OperationPoint>,
    start_date: u32,
    end_date: u32,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct OperationPointsPayload {
    operation_points: Vec<OperationPoint>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SignalGroup {
    pub long_signals: Vec<u32>,
    pub short_signals: Vec<u32>,
}

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct OperationPoint {
    instrument: String,
    result: i32,
    tp: i32,
    risk: f64,
    money_management_strategy_id: i32,
    id: i32,
    sl: i32,
    timestamp: u32,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Strategy {
    annual_roi: f64,
    max_draw_down: f64,
    annual_operation_count: f64,
    money_management_strategy_id: u32,
    indicator_id: u32,
}
