use crate::strategies::OperationPoint;
use actix_web::{web, HttpResponse, Responder};
use chrono::NaiveDate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct AnnualRoiPayload {
    operation_points: Vec<OperationPoint>,
    start_date: NaiveDate,
    end_date: NaiveDate,
}

pub async fn annual_roi(payload: web::Json<AnnualRoiPayload>) -> impl Responder {
    let annual_roi: f64 = get_annual_roi(
        &payload.operation_points,
        payload.start_date,
        payload.end_date,
    );
    HttpResponse::Ok().json(serde_json::json!({ "data": annual_roi }))
}

pub fn get_annual_roi(
    operation_points: &Vec<OperationPoint>,
    start_date: NaiveDate,
    end_date: NaiveDate,
) -> f64 {
    0.0
}
