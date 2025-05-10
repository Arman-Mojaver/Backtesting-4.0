pub mod annual_operation_count;
pub mod annual_roi;
pub mod global_roi;
pub mod max_draw_down;
pub mod operation_points_map;

use actix_web::{web, HttpResponse, Responder};
use chrono::NaiveDate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct OperationPointsWithDatesPayload {
    operation_points: Vec<OperationPoint>,
    start_date: NaiveDate,
    end_date: NaiveDate,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct OperationPointsPayload {
    operation_points: Vec<OperationPoint>,
}

#[derive(Debug, Deserialize)]
pub struct RequestPayloadStrategy {}

#[derive(Debug, Serialize, Deserialize)]
pub struct OperationPoint {
    instrument: String,
    result: i32,
    tp: i32,
    risk: f64,
    money_management_strategy_id: i32,
    datetime: NaiveDate,
    id: i32,
    sl: i32,
}

pub async fn process_strategies(
    _request_body: web::Json<RequestPayloadStrategy>,
) -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "data": [] }))
}
