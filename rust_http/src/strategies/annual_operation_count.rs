use crate::strategies::RequestPayloadStrategy;
use actix_web::{web, HttpResponse, Responder};
use chrono::NaiveDate;
use log::info;
use serde::{Deserialize, Serialize};

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

#[derive(Debug, Serialize, Deserialize)]
pub struct OperationPointPayload {
    data: Vec<OperationPoint>,
}


pub async fn annual_operation_count(
    payload: web::Json<OperationPointPayload>,
) -> impl Responder {
    let annual_operation_count = get_annual_operation_count(&payload.data);
    HttpResponse::Ok().json(serde_json::json!({ "data": annual_operation_count }))
}


pub fn get_annual_operation_count(operation_points: &Vec<OperationPoint>) -> i32 {
    0
}
