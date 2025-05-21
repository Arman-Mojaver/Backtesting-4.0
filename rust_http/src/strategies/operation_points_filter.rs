use crate::strategies::{OperationPoint, SignalGroup};
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use std::sync::Arc;

#[derive(Debug, Serialize, Deserialize)]
pub struct OperationPointsFilterPayload {
    long_operation_points_table: Vec<(i32, OperationPoint)>,
    short_operation_points_table: Vec<(i32, OperationPoint)>,
    signal_group: SignalGroup,
}

pub struct OperationPointsGroup {
    pub operation_points: Vec<Arc<OperationPoint>>,
    pub long_operation_point_ids: Vec<i32>,
    pub short_operation_point_ids: Vec<i32>,
}

pub async fn operation_points_filter(
    payload: web::Json<OperationPointsFilterPayload>,
) -> impl Responder {
    let payload = payload.into_inner();

    let mut long_table: Vec<(i32, Arc<OperationPoint>)> = payload
        .long_operation_points_table
        .into_iter()
        .map(|(ts, op)| (ts, Arc::new(op)))
        .collect();
    long_table.sort_unstable_by_key(|&(ts, _)| ts);

    let mut short_table: Vec<(i32, Arc<OperationPoint>)> = payload
        .short_operation_points_table
        .into_iter()
        .map(|(ts, op)| (ts, Arc::new(op)))
        .collect();
    short_table.sort_unstable_by_key(|&(ts, _)| ts);

    let operation_points_group =
        get_operation_points_filter(&long_table, &short_table, &payload.signal_group);

    let serialized_operation_points: Vec<OperationPoint> = operation_points_group
        .operation_points
        .into_iter()
        .map(|arc| (*arc).clone())
        .collect();

    HttpResponse::Ok().json(serde_json::json!(
        { "data":
            {
                "operation_points": serialized_operation_points,
                "long_operation_point_ids": operation_points_group.long_operation_point_ids,
                "short_operation_point_ids": operation_points_group.short_operation_point_ids,
            }
        }
    ))
}

fn lookup_operation_points<'a>(
    timestamps: &[i32],
    operation_points_table: &'a [(i32, Arc<OperationPoint>)],
) -> Vec<&'a Arc<OperationPoint>> {
    let mut operation_points = Vec::with_capacity(timestamps.len());
    let mut table_index = 0;
    let n = operation_points_table.len();

    for &timestamp in timestamps {
        while table_index < n && operation_points_table[table_index].0 < timestamp {
            table_index += 1;
        }

        operation_points.push(&operation_points_table[table_index].1);
    }
    operation_points
}

pub fn get_operation_points_filter(
    long_operation_points_table: &Vec<(i32, Arc<OperationPoint>)>,
    short_operation_points_table: &Vec<(i32, Arc<OperationPoint>)>,
    signal_group: &SignalGroup,
) -> OperationPointsGroup {
    let mut operation_points: Vec<Arc<OperationPoint>> =
        Vec::with_capacity(signal_group.long_signals.len() + signal_group.short_signals.len());

    let long_operation_points =
        lookup_operation_points(&signal_group.long_signals, long_operation_points_table);
    let short_operation_points =
        lookup_operation_points(&signal_group.short_signals, short_operation_points_table);

    let long_operation_point_ids = long_operation_points.iter().map(|p| p.id).collect();
    let short_operation_point_ids = short_operation_points.iter().map(|p| p.id).collect();

    operation_points.extend(long_operation_points.into_iter().cloned());
    operation_points.extend(short_operation_points.into_iter().cloned());

    operation_points.sort_by_key(|p| p.timestamp);
    OperationPointsGroup {
        operation_points,
        long_operation_point_ids,
        short_operation_point_ids,
    }
}
