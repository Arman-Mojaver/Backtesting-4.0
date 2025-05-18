use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct QueryIndicatorsPayload {
    type_: String,
}

pub async fn query_indicators(payload: web::Json<QueryIndicatorsPayload>) -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "data": [] }))
}

pub async fn get_query_indicators() -> i32 {
    0
}
