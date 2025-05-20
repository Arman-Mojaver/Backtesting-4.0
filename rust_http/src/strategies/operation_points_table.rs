use crate::strategies::{OperationPoint, OperationPointsPayload};
use actix_web::{web, HttpResponse, Responder};
use std::collections::HashMap;
use std::sync::Arc;

pub async fn operation_points_table(payload: web::Json<OperationPointsPayload>) -> impl Responder {
    let payload = payload.into_inner();
    let operation_points_table = get_operation_points_table(&payload.operation_points);

    let serialized_operation_points: HashMap<i32, OperationPoint> = operation_points_table
        .iter()
        .map(|(ts, op_arc)| (*ts, (**op_arc).clone()))
        .collect();

    HttpResponse::Ok().json(serde_json::json!({"data": serialized_operation_points}))
}

pub fn get_operation_points_table(
    operation_points: &Vec<OperationPoint>,
) -> Arc<Vec<(i32, Arc<OperationPoint>)>> {
    let mut table: Vec<(i32, Arc<OperationPoint>)> = operation_points
        .iter()
        .map(|op| (op.timestamp, Arc::new(op.clone())))
        .collect();

    table.sort_unstable_by_key(|entry| entry.0);
    Arc::new(table)
}
