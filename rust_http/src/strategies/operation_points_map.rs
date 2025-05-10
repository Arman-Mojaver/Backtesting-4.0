use crate::strategies::{OperationPoint, OperationPointsPayload};
use actix_web::{web, HttpResponse, Responder};
use std::collections::HashMap;

pub async fn operation_points_map(payload: web::Json<OperationPointsPayload>) -> impl Responder {
    let payload = payload.into_inner();
    let operation_points_map = get_operation_points_map(payload.operation_points);

    HttpResponse::Ok().json(serde_json::json!({ "data": operation_points_map }))
}

pub fn get_operation_points_map(
    operation_points: Vec<OperationPoint>,
) -> HashMap<String, OperationPoint> {
    operation_points
        .into_iter()
        .map(|op| {
            let date_str = op.datetime.format("%Y-%m-%d").to_string();
            (date_str, op)
        })
        .collect()
}
