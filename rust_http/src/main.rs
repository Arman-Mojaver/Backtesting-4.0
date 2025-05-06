use actix_web::{web, App, HttpResponse, HttpServer};
use chrono::Local;
use fern::colors::{Color, ColoredLevelConfig};
use log::info;
use std::io;

mod indicators;
mod routes;
mod strategies;

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

fn configure_routes(cfg: &mut web::ServiceConfig) {
    cfg
        // process_strategies
        .route(
            "/process_strategies",
            web::post().to(strategies::process_strategies),
        )
        .route(
            "/process_strategies",
            web::get().to(routes::method_not_allowed),
        )
        .route(
            "/process_strategies",
            web::put().to(routes::method_not_allowed),
        )
        .route(
            "/process_strategies",
            web::delete().to(routes::method_not_allowed),
        )
        // rsi
        .route("/rsi", web::post().to(indicators::rsi::rsi))
        .route("/rsi", web::get().to(routes::method_not_allowed))
        .route("/rsi", web::put().to(routes::method_not_allowed))
        .route("/rsi", web::delete().to(routes::method_not_allowed))
        // General routes
        .service(routes::ping)
        .default_service(web::route().to(routes::index))
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

#[actix_web::main]
async fn main() -> io::Result<()> {
    // Initialize logger
    if let Err(e) = setup_logger() {
        eprintln!("Error initializing logger: {}", e);
        std::process::exit(1);
    }

    let host = std::env::var("HOST").unwrap_or_else(|_| "0.0.0.0:81".into());
    info!("Server starting on {}", &host);

    HttpServer::new(|| App::new().configure(configure_routes))
        .workers(7)
        .bind(&host)?
        .run()
        .await
}
