use crate::strategies::{OperationPoint, OperationPointsPayload};
use actix_web::{web, HttpResponse, Responder};

pub async fn global_roi(payload: web::Json<OperationPointsPayload>) -> impl Responder {
    let operation_point_references: Vec<&OperationPoint> =
        payload.operation_points.iter().collect();
    let global_roi: f64 = get_global_roi(&operation_point_references);
    HttpResponse::Ok().json(serde_json::json!({ "data": global_roi }))
}

pub fn get_global_roi(operation_points: &Vec<&OperationPoint>) -> f64 {
    let mut cumsum: f64 = 1.0;
    for point in operation_points {
        let result = point.result as f64 * (point.risk / point.sl as f64);
        cumsum += result;
    }
    ((cumsum - 1.0) * 10000.0).round() / 100.0
}
