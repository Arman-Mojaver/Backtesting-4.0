use actix_web::{web, HttpResponse, Responder};
use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct RequestPayloadRsi {}

pub async fn rsi(_request_body: web::Json<RequestPayloadRsi>) -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "data": [] }))
}
