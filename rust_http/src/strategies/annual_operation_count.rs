use crate::strategies::OperationPoint;
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use std::sync::Arc;

#[derive(Debug, Serialize, Deserialize)]
pub struct AnnualOperationCountPayload {
    operation_points: Vec<OperationPoint>,
    start_date: i32,
    end_date: i32,
}

pub async fn annual_operation_count(
    payload: web::Json<AnnualOperationCountPayload>,
) -> impl Responder {
    let operation_points_references: Vec<Arc<OperationPoint>> = payload
        .operation_points
        .iter()
        .cloned()
        .map(Arc::new)
        .collect();

    let annual_operation_count = get_annual_operation_count(
        &operation_points_references,
        payload.start_date,
        payload.end_date,
    );
    HttpResponse::Ok().json(serde_json::json!({ "data": annual_operation_count }))
}

pub fn get_annual_operation_count(
    operation_points: &Vec<Arc<OperationPoint>>,
    start_date: i32,
    end_date: i32,
) -> f64 {
    let count = operation_points.len();
    if count == 0 {
        return 0.0;
    }

    let mut dates: Vec<i32> = operation_points.iter().map(|op| op.timestamp).collect();
    dates.sort_unstable();

    let duration_secs = end_date - start_date;
    let days = duration_secs / (24 * 60 * 60);
    if days == 0 {
        return 0.0;
    }

    let annualized = (count as f64 / days as f64) * 365.25;
    (annualized * 100.0).round() / 100.0
}
