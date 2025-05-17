use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct QueryOperationPointsPayload {
    money_management_strategy_id: i32,
}

pub async fn query_short_operation_points(
    payload: web::Json<QueryOperationPointsPayload>,
) -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "data": [] }))
}

pub async fn get_query_short_operation_points() -> i32 {
    0
}
