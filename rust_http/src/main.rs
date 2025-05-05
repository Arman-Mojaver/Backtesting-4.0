use actix_web::{
    dev::ServiceRequest, dev::ServiceResponse, get, http::Method, middleware::ErrorHandlerResponse,
    middleware::ErrorHandlers, post, web, App, Error, HttpResponse, HttpServer, Responder,
};
use chrono::Local;
use fern::colors::{Color, ColoredLevelConfig};
use log::info;
use serde::Deserialize;
use serde::Serialize;
use std::io;

#[derive(Debug, Deserialize)]
struct RequestPayload {}

async fn process_strategies(request_body: web::Json<RequestPayload>) -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "data": [] }))
}

async fn rsi(request_body: web::Json<RequestPayload>) -> impl Responder {
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

// -- logger setup --
fn setup_logger() -> Result<(), fern::InitError> {
    let colors = ColoredLevelConfig::new()
        .error(Color::Red)
        .warn(Color::Yellow)
        .info(Color::Green)
        .debug(Color::Blue)
        .trace(Color::Magenta);

    let log_file = fern::log_file("logs/rust-http.log")?;

    fern::Dispatch::new()
        .level(log::LevelFilter::Off)
        .level_for("rust_http", log::LevelFilter::Info)
        .chain(
            fern::Dispatch::new()
                .format(move |out, message, record| {
                    out.finish(format_args!(
                        "{} [{}] [{}:{}] {}",
                        Local::now().format("%Y/%m/%d %H:%M:%S"),
                        colors.color(record.level()),
                        record.file().unwrap_or("unknown"),
                        record.line().unwrap_or(0),
                        message
                    ))
                })
                .chain(io::stdout()),
        )
        .chain(
            fern::Dispatch::new()
                .format(move |out, message, record| {
                    out.finish(format_args!(
                        "{} [{}] [{}:{}] {}",
                        Local::now().format("%Y/%m/%d %H:%M:%S"),
                        record.level(), // no ANSI color in file
                        record.file().unwrap_or("unknown"),
                        record.line().unwrap_or(0),
                        message
                    ))
                })
                .chain(log_file),
        )
        .apply()?;

    Ok(())
}

#[actix_web::main]
async fn main() -> io::Result<()> {
    // Initialize logger
    if let Err(e) = setup_logger() {
        eprintln!("Error initializing logger: {}", e);
        std::process::exit(1);
    }

    let host = std::env::var("HOST").unwrap_or_else(|_| "0.0.0.0:81".into());
    info!("Server starting on {}", &host);

    HttpServer::new(|| {
        App::new()
            .app_data(web::JsonConfig::default().error_handler(|err, _req| {
                actix_web::error::InternalError::from_response(
                    err,
                    HttpResponse::BadRequest().json(serde_json::json!({
                        "error": "Invalid JSON"
                    })),
                )
                .into()
            }))
            .route("/process_strategies", web::post().to(process_strategies))
            .route("/process_strategies", web::get().to(method_not_allowed))
            .route("/process_strategies", web::put().to(method_not_allowed))
            .route("/process_strategies", web::delete().to(method_not_allowed))
            .route("/rsi", web::post().to(rsi))
            .route("/rsi", web::get().to(method_not_allowed))
            .route("/rsi", web::put().to(method_not_allowed))
            .route("/rsi", web::delete().to(method_not_allowed))
            .service(ping)
            .default_service(web::route().to(index))
    })
    .workers(7)
    .bind(&host)?
    .run()
    .await
}
