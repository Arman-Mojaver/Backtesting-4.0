use crate::strategies::{OperationPoint, SignalGroup};
use actix_web::{web, HttpResponse, Responder};
use rustc_hash::FxHashMap;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;

#[derive(Debug, Serialize, Deserialize)]
pub struct OperationPointsFilterPayload {
    long_operation_points_map: HashMap<i32, OperationPoint>,
    short_operation_points_map: HashMap<i32, OperationPoint>,
    signal_group: SignalGroup,
}

pub async fn operation_points_filter(
    payload: web::Json<OperationPointsFilterPayload>,
) -> impl Responder {
    let payload = payload.into_inner();

    let long_operation_points_map: FxHashMap<i32, Arc<OperationPoint>> = payload
        .long_operation_points_map
        .into_iter()
        .map(|(k, v)| (k, Arc::new(v)))
        .collect();

    let short_operation_points_map: FxHashMap<i32, Arc<OperationPoint>> = payload
        .short_operation_points_map
        .into_iter()
        .map(|(k, v)| (k, Arc::new(v)))
        .collect();

    let operation_point_list = get_operation_points_filter(
        &long_operation_points_map,
        &short_operation_points_map,
        &payload.signal_group,
    );

    let serialized_operation_points: Vec<&OperationPoint> =
        operation_point_list.iter().map(|arc| &**arc).collect();

    HttpResponse::Ok().json(serde_json::json!({ "data": serialized_operation_points }))
}

pub fn get_operation_points_filter(
    long_operation_points_map: &FxHashMap<i32, Arc<OperationPoint>>,
    short_operation_points_map: &FxHashMap<i32, Arc<OperationPoint>>,
    signal_group: &SignalGroup,
) -> Vec<Arc<OperationPoint>> {
    let mut operation_points: Vec<Arc<OperationPoint>> = Vec::new();

    operation_points.extend(
        signal_group
            .long_signals
            .iter()
            .filter_map(|sig| long_operation_points_map.get(sig).cloned()),
    );

    operation_points.extend(
        signal_group
            .short_signals
            .iter()
            .filter_map(|sig| short_operation_points_map.get(sig).cloned()),
    );

    operation_points.sort_by_key(|p| p.timestamp);
    operation_points
}
