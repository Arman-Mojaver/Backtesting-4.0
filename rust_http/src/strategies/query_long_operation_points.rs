use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct QueryLongOperationPointsPayload {
    money_management_strategy_id: i32,
}

pub async fn query_long_operation_points(
    payload: web::Json<QueryLongOperationPointsPayload>,
) -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "data": [] }))
}

pub async fn get_query_long_operation_points() -> i32 {
    0
}
