use crate::strategies::OperationPoint;
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct MaxDrawDownPayload {
    operation_points: Vec<OperationPoint>,
}

pub async fn max_draw_down(payload: web::Json<MaxDrawDownPayload>) -> impl Responder {
    let max_draw_down = get_max_draw_down(&payload.operation_points);
    HttpResponse::Ok().json(serde_json::json!({ "data": max_draw_down }))
}

pub fn get_max_draw_down(operation_points: &Vec<OperationPoint>) -> f64 {
    let mut cumsum: f64 = 1.0;
    let mut cummax: f64 = 1.0;
    let mut draw_downs: Vec<f64> = Vec::new();

    for point in operation_points.iter() {
        let result: f64 = point.result as f64 * point.risk / point.sl as f64;
        cumsum += result;
        cummax = cummax.max(cumsum);
        let draw_down: f64 = (cummax - cumsum) / cummax;
        let rounded_draw_down: f64 = (draw_down * 10000.0).round() / 100.0;
        draw_downs.push(rounded_draw_down);
    }
    get_max(&draw_downs)
}

fn get_max(floats: &Vec<f64>) -> f64 {
    let mut max_value: f64 = 0.0;
    for float in floats.iter() {
        max_value = max_value.max(*float);
    }
    max_value
}
