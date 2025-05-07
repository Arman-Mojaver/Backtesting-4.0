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
    0.0
}
