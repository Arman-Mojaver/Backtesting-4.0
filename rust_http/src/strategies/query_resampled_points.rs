use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct QueryResampledPointsPayload {
    instrument: String,
}

pub async fn query_resampled_points(
    payload: web::Json<QueryResampledPointsPayload>,
) -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "data": [] }))
}

pub async fn get_query_resampled_points() -> i32 {
    0
}
