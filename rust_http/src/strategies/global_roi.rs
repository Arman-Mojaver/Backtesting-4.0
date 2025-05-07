use crate::strategies::{OperationPoint, OperationPointsPayload};
use actix_web::{web, HttpResponse, Responder};


pub async fn global_roi(payload: web::Json<OperationPointsPayload>) -> impl Responder {
    let global_roi: f64 = get_global_roi(&payload.operation_points);
    HttpResponse::Ok().json(serde_json::json!({ "data": global_roi }))
}

pub fn get_global_roi(operation_points: &Vec<OperationPoint>) -> f64 {
    0.0
}
