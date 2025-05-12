use crate::strategies::{OperationPoint, SignalGroup};
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Debug, Serialize, Deserialize)]
pub struct OperationPointsFilterPayload {
    long_operation_points_map: HashMap<u32, OperationPoint>,
    short_operation_points_map: HashMap<u32, OperationPoint>,
    signal_group: SignalGroup,
}

pub async fn operation_points_filter(
    payload: web::Json<OperationPointsFilterPayload>,
) -> impl Responder {
    let payload = payload.into_inner();
    let operation_point_list = get_operation_points_filter(
        &payload.long_operation_points_map,
        &payload.short_operation_points_map,
        &payload.signal_group,
    );

    HttpResponse::Ok().json(serde_json::json!({ "data": operation_point_list }))
}

pub fn get_operation_points_filter<'a>(
    long_operation_points_map: &'a HashMap<u32, OperationPoint>,
    short_operation_points_map: &'a HashMap<u32, OperationPoint>,
    signal_group: &SignalGroup,
) -> Vec<&'a OperationPoint> {
    let mut operation_points: Vec<&OperationPoint> = Vec::new();

    operation_points.extend(
        signal_group
            .long_signals
            .iter()
            .filter_map(|sig| long_operation_points_map.get(sig)),
    );

    operation_points.extend(
        signal_group
            .short_signals
            .iter()
            .filter_map(|sig| short_operation_points_map.get(sig)),
    );

    operation_points.sort_by_key(|p| p.timestamp);
    operation_points
}
