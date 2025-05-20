use crate::strategies::OperationPoint;
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct ProcessStrategiesValidatorPayload {
    long_operation_points: Vec<(OperationPoint)>,
    short_operation_points: Vec<(OperationPoint)>,
    money_management_strategy_id: i32,
}

#[derive(Debug)]
enum ValidationError {}

pub async fn process_strategies_validator(
    payload: web::Json<ProcessStrategiesValidatorPayload>,
) -> impl Responder {
    match get_process_strategies_validator(
        &payload.long_operation_points,
        &payload.short_operation_points,
        payload.money_management_strategy_id,
    ) {
        Ok(()) => HttpResponse::Ok().json(serde_json::json!({ "data": "OK!" })),
        Err(_) => HttpResponse::Ok().json(serde_json::json!({ "data": "ERROR!" })),
    }
}

pub fn get_process_strategies_validator(
    long_operation_points: &Vec<(OperationPoint)>,
    short_operation_points: &Vec<(OperationPoint)>,
    money_management_strategy_id: i32,
) -> Result<(), ValidationError> {
    Ok(())
}
