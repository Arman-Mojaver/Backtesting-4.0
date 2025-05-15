use crate::strategies::{OperationPoint, OperationPointsPayload};
use actix_web::{web, HttpResponse, Responder};
use std::sync::Arc;

pub async fn max_draw_down(payload: web::Json<OperationPointsPayload>) -> impl Responder {
    let operation_point_references: Vec<Arc<OperationPoint>> = payload
        .operation_points
        .iter()
        .map(|point| Arc::new(point.clone()))
        .collect();

    let max_draw_down = get_max_draw_down(&operation_point_references);
    HttpResponse::Ok().json(serde_json::json!({ "data": max_draw_down }))
}

pub fn get_max_draw_down(operation_points: &Vec<Arc<OperationPoint>>) -> f64 {
    let mut cumsum: f64 = 1.0;
    let mut cummax: f64 = 1.0;
    let mut draw_downs: Vec<f64> = Vec::new();

    for point in operation_points {
        let result: f64 = point.result as f64 * point.risk / point.sl as f64;
        cumsum += result;
        cummax = cummax.max(cumsum);
        let draw_down: f64 = (cummax - cumsum) / cummax;
        let rounded_draw_down: f64 = (draw_down * 10000.0).round() / 100.0;
        draw_downs.push(rounded_draw_down);
    }
    get_max(&draw_downs)
}

fn get_max(floats: &[f64]) -> f64 {
    floats.iter().copied().fold(0.0, f64::max)
}
