use actix_web::{get, web, HttpResponse, Responder};
use log::info;
use serde::Serialize;

pub async fn method_not_allowed() -> impl Responder {
    HttpResponse::MethodNotAllowed().json(serde_json::json!({
        "error": "Method Not Allowed"
    }))
}

pub async fn index() -> impl Responder {
    HttpResponse::NotFound().json(PingResponse {
        message: "Server Working. Endpoint not defined!".into(),
    })
}

#[derive(Serialize)]
struct PingResponse {
    message: String,
}

#[get("/ping")]
pub async fn ping() -> impl Responder {
    info!("GET /ping");
    web::Json(PingResponse {
        message: "Ping!".into(),
    })
}
