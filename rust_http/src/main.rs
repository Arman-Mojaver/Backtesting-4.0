use actix_web::{web, App, HttpResponse, HttpServer};
use chrono::Local;
use fern::colors::{Color, ColoredLevelConfig};
use log::info;
use std::io;

mod indicators;
mod routes;
mod strategies;

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
        //
        // rsi
        //
        .route("/rsi", web::post().to(indicators::rsi::rsi))
        .route("/rsi", web::get().to(routes::method_not_allowed))
        .route("/rsi", web::put().to(routes::method_not_allowed))
        .route("/rsi", web::delete().to(routes::method_not_allowed))
        // General routes
        .service(routes::ping)
        .default_service(web::route().to(routes::index))
        //
        // Invalid JSON error handler
        //
        .app_data(web::JsonConfig::default().error_handler(|err, _req| {
            actix_web::error::InternalError::from_response(
                err,
                HttpResponse::BadRequest().json(serde_json::json!({
                    "error": "Invalid JSON"
                })),
            )
            .into()
        }))
        //
        // Test endpoints
        //
        .route(
            "/annual_operation_count",
            web::post().to(strategies::annual_operation_count::annual_operation_count),
        )
        .route(
            "/annual_operation_count",
            web::get().to(routes::method_not_allowed),
        )
        .route(
            "/annual_operation_count",
            web::put().to(routes::method_not_allowed),
        )
        .route(
            "/annual_operation_count",
            web::delete().to(routes::method_not_allowed),
        )
        .route(
            "/max_draw_down",
            web::post().to(strategies::max_draw_down::max_draw_down),
        )
        .route("/max_draw_down", web::get().to(routes::method_not_allowed))
        .route("/max_draw_down", web::put().to(routes::method_not_allowed))
        .route(
            "/max_draw_down",
            web::delete().to(routes::method_not_allowed),
        )
        .route(
            "/global_roi",
            web::post().to(strategies::global_roi::global_roi),
        )
        .route("/global_roi", web::get().to(routes::method_not_allowed))
        .route("/global_roi", web::put().to(routes::method_not_allowed))
        .route("/global_roi", web::delete().to(routes::method_not_allowed))
        .route(
            "/annual_roi_from_global_roi",
            web::post().to(strategies::annual_roi_from_global_roi::annual_roi_from_global_roi),
        )
        .route(
            "/annual_roi_from_global_roi",
            web::get().to(routes::method_not_allowed),
        )
        .route(
            "/annual_roi_from_global_roi",
            web::put().to(routes::method_not_allowed),
        )
        .route(
            "/annual_roi_from_global_roi",
            web::delete().to(routes::method_not_allowed),
        )
        .route(
            "/operation_points_map",
            web::post().to(strategies::operation_points_map::operation_points_map),
        )
        .route(
            "/operation_points_map",
            web::get().to(routes::method_not_allowed),
        )
        .route(
            "/operation_points_map",
            web::put().to(routes::method_not_allowed),
        )
        .route(
            "/operation_points_map",
            web::delete().to(routes::method_not_allowed),
        )
        .route(
            "/operation_points_filter",
            web::post().to(strategies::operation_points_filter::operation_points_filter),
        )
        .route(
            "/operation_points_filter",
            web::get().to(routes::method_not_allowed),
        )
        .route(
            "/operation_points_filter",
            web::put().to(routes::method_not_allowed),
        )
        .route(
            "/operation_points_filter",
            web::delete().to(routes::method_not_allowed),
        )
        .route(
            "/process_strategy",
            web::post().to(strategies::process_strategy::process_strategy),
        )
        .route(
            "/process_strategy",
            web::get().to(routes::method_not_allowed),
        )
        .route(
            "/process_strategy",
            web::put().to(routes::method_not_allowed),
        )
        .route(
            "/process_strategy",
            web::delete().to(routes::method_not_allowed),
        );
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
