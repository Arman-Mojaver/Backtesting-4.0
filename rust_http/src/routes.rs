use actix_web::{get, web, HttpResponse, Responder};
use log::info;
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize)]
struct RequestPayload {}

async fn process_strategies(_request_body: web::Json<RequestPayload>) -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "data": [] }))
}

async fn rsi(_request_body: web::Json<RequestPayload>) -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "data": [] }))
}

async fn method_not_allowed() -> impl Responder {
    HttpResponse::MethodNotAllowed().json(serde_json::json!({
        "error": "Method Not Allowed"
    }))
}

async fn index() -> impl Responder {
    HttpResponse::NotFound().json(PingResponse {
        message: "Server Working. Endpoint not defined!".into(),
    })
}

#[derive(Serialize)]
struct PingResponse {
    message: String,
}

#[get("/ping")]
async fn ping() -> impl Responder {
    info!("GET /ping");
    web::Json(PingResponse {
        message: "Ping!".into(),
    })
}

pub fn configure_routes(cfg: &mut web::ServiceConfig) {
    cfg
        // process_strategies
        .route("/process_strategies", web::post().to(process_strategies))
        .route("/process_strategies", web::get().to(method_not_allowed))
        .route("/process_strategies", web::put().to(method_not_allowed))
        .route("/process_strategies", web::delete().to(method_not_allowed))
        // rsi
        .route("/rsi", web::post().to(rsi))
        .route("/rsi", web::get().to(method_not_allowed))
        .route("/rsi", web::put().to(method_not_allowed))
        .route("/rsi", web::delete().to(method_not_allowed))
        // General routes
        .service(ping)
        .default_service(web::route().to(index))
        // Invalid JSON error handler
        .app_data(web::JsonConfig::default().error_handler(|err, _req| {
            actix_web::error::InternalError::from_response(
                err,
                HttpResponse::BadRequest().json(serde_json::json!({
                    "error": "Invalid JSON"
                })),
            )
            .into()
        }));
}
