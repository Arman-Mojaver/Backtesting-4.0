use crate::strategies::OperationPoint;
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct GlobalRoiPayload {
    operation_points: Vec<OperationPoint>,
}

pub async fn global_roi(payload: web::Json<GlobalRoiPayload>) -> impl Responder {
    let global_roi: f64 = get_global_roi(&payload.operation_points);
    HttpResponse::Ok().json(serde_json::json!({ "data": global_roi }))
}

pub fn get_global_roi(operation_points: &Vec<OperationPoint>) -> f64 {
    0.0
}
