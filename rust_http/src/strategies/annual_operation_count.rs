use crate::strategies::{OperationPoint, OperationPointsWithDatesPayload};
use actix_web::{web, HttpResponse, Responder};
use chrono::NaiveDate;

pub async fn annual_operation_count(
    payload: web::Json<OperationPointsWithDatesPayload>,
) -> impl Responder {

    let operation_points_references: Vec<&OperationPoint> = payload
        .operation_points
        .iter()
        .collect();


    let annual_operation_count = get_annual_operation_count(
        operation_points_references,
        payload.start_date,
        payload.end_date,
    );
    HttpResponse::Ok().json(serde_json::json!({ "data": annual_operation_count }))
}

pub fn get_annual_operation_count(
    operation_points: Vec<&OperationPoint>,
    start_date: NaiveDate,
    end_date: NaiveDate,
) -> f64 {
    let count = operation_points.len();
    if count == 0 {
        return 0.0;
    }

    let mut dates: Vec<NaiveDate> = operation_points.iter().map(|op| op.datetime).collect();
    dates.sort_unstable();

    let days = end_date.signed_duration_since(start_date).num_days() as f64;
    if days <= 0.0 {
        return 0.0;
    }

    let annualized = (count as f64 / days) * 365.25;
    let count = (annualized * 100.0).round() / 100.0;
    count
}
