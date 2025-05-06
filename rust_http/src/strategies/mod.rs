use actix_web::{web, HttpResponse, Responder};
use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct RequestPayloadStrategy {}

pub async fn process_strategies(
    _request_body: web::Json<RequestPayloadStrategy>,
) -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "data": [] }))
}
