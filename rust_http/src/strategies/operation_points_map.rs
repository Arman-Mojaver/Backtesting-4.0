use crate::strategies::{OperationPoint, OperationPointsPayload};
use actix_web::{web, HttpResponse, Responder};
use rustc_hash::FxHashMap;
use std::collections::HashMap;
use std::sync::Arc;

pub async fn operation_points_map(payload: web::Json<OperationPointsPayload>) -> impl Responder {
    let payload = payload.into_inner();
    let operation_points_map = get_operation_points_map(&payload.operation_points);

    let serialized_operation_points_map: HashMap<i32, OperationPoint> = operation_points_map
        .iter()
        .map(|(&ts, op_arc)| (ts, (**op_arc).clone()))
        .collect();

    HttpResponse::Ok().json(serde_json::json!({ "data": serialized_operation_points_map }))
}

pub fn get_operation_points_map(
    operation_points: &Vec<OperationPoint>,
) -> Arc<FxHashMap<i32, Arc<OperationPoint>>> {
    let map: FxHashMap<i32, Arc<OperationPoint>> = operation_points
        .iter()
        .map(|op| (op.timestamp, Arc::new(op.clone())))
        .collect();

    Arc::new(map)
}
