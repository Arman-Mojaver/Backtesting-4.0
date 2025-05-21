use crate::strategies::{Indicator, OperationPoint};
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use std::collections::HashSet;

#[derive(Debug, Serialize, Deserialize)]
pub struct ProcessStrategiesValidatorPayload {
    long_operation_points: Vec<OperationPoint>,
    short_operation_points: Vec<OperationPoint>,
    money_management_strategy_id: i32,
    indicators: Vec<Indicator>,
}

#[derive(Debug)]
pub enum ValidationError {
    Empty,
    InstrumentMismatch,
    MoneyManagementStrategyIdMismatch,
    TimestampMismatch,
}

pub async fn process_strategies_validator(
    payload: web::Json<ProcessStrategiesValidatorPayload>,
) -> impl Responder {
    match get_process_strategies_validator(
        &payload.long_operation_points,
        &payload.short_operation_points,
        payload.money_management_strategy_id,
        &payload.indicators,
    ) {
        Ok(()) => HttpResponse::Ok().json(serde_json::json!({ "data": "OK!" })),
        Err(_) => {
            HttpResponse::Ok().json(serde_json::json!({ "error": "process_strategies_validator" }))
        }
    }
}

pub fn get_process_strategies_validator(
    long_operation_points: &Vec<OperationPoint>,
    short_operation_points: &Vec<OperationPoint>,
    money_management_strategy_id: i32,
    indicators: &Vec<Indicator>,
) -> Result<(), ValidationError> {
    validate_not_empty(long_operation_points)?;
    validate_not_empty(short_operation_points)?;
    validate_same_instrument(long_operation_points, short_operation_points)?;
    validate_strategy_id_matches(
        long_operation_points,
        short_operation_points,
        money_management_strategy_id,
    )?;
    validate_matching_timestamps(long_operation_points, short_operation_points)?;
    validate_same_indicator_type(indicators)?;

    Ok(())
}

fn validate_not_empty(points: &Vec<OperationPoint>) -> Result<(), ValidationError> {
    if points.is_empty() {
        return Err(ValidationError::Empty);
    }
    Ok(())
}

fn validate_same_instrument(
    long_points: &Vec<OperationPoint>,
    short_points: &Vec<OperationPoint>,
) -> Result<(), ValidationError> {
    let reference = &long_points[0].instrument;

    if long_points
        .iter()
        .chain(short_points.iter())
        .any(|op| &op.instrument != reference)
    {
        return Err(ValidationError::InstrumentMismatch);
    }

    Ok(())
}

fn validate_strategy_id_matches(
    long_points: &Vec<OperationPoint>,
    short_points: &Vec<OperationPoint>,
    expected_id: i32,
) -> Result<(), ValidationError> {
    if long_points
        .iter()
        .chain(short_points.iter())
        .any(|op| op.money_management_strategy_id != expected_id)
    {
        return Err(ValidationError::MoneyManagementStrategyIdMismatch);
    }

    Ok(())
}

fn validate_matching_timestamps(
    long_points: &Vec<OperationPoint>,
    short_points: &Vec<OperationPoint>,
) -> Result<(), ValidationError> {
    let long_timestamps: HashSet<i32> = long_points.iter().map(|op| op.timestamp).collect();
    let short_timestamps: HashSet<i32> = short_points.iter().map(|op| op.timestamp).collect();

    if long_timestamps != short_timestamps {
        return Err(ValidationError::TimestampMismatch);
    }

    Ok(())
}

fn validate_same_indicator_type(indicators: &Vec<Indicator>) -> Result<(), ValidationError> {
    let reference = &indicators[0].r#type;

    if indicators.iter().any(|i| &i.r#type != reference) {
        return Err(ValidationError::InstrumentMismatch);
    }

    Ok(())
}
