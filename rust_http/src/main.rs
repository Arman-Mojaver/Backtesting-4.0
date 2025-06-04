use actix_web::{web, App, FromRequest, HttpResponse, HttpServer, Responder};
use chrono::Local;
use fern::colors::{Color, ColoredLevelConfig};
use log::info;
use std::future::Future;
use std::io;

mod config;
mod db;
mod routes;
mod signals;
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

fn post_only_route<F, Fut, T, R>(cfg: &mut web::ServiceConfig, path: &str, handler: F)
where
    F: Fn(T) -> Fut + Clone + 'static,
    Fut: Future<Output = R> + 'static,
    T: FromRequest + 'static,
    R: Responder + 'static,
{
    cfg.service(
        web::resource(path)
            .route(web::post().to(handler.clone()))
            .route(web::get().to(routes::method_not_allowed))
            .route(web::put().to(routes::method_not_allowed))
            .route(web::delete().to(routes::method_not_allowed)),
    );
}

fn configure_routes(cfg: &mut web::ServiceConfig) {
    cfg.service(routes::ping)
        .default_service(web::route().to(routes::index))
        .app_data(
            web::JsonConfig::default()
                .limit(2048 * 1024 * 1024) // 2048 MB
                .error_handler(|err, _req| {
                    actix_web::error::InternalError::from_response(
                        err,
                        HttpResponse::BadRequest().json(serde_json::json!({
                            "error": "Invalid JSON"
                        })),
                    )
                    .into()
                }),
        );

    // Production Endpoints
    post_only_route(
        cfg,
        "/process_strategies",
        strategies::process_strategies::process_strategies,
    );

    // Test Endpoints
    post_only_route(
        cfg,
        "/process_strategies_test",
        strategies::process_strategies_test::process_strategies_test,
    );
    post_only_route(
        cfg,
        "/process_strategies_from_signals_test",
        strategies::process_strategies_from_signals::process_strategies_from_signals,
    );
    post_only_route(
        cfg,
        "/annual_operation_count_test",
        strategies::annual_operation_count::annual_operation_count,
    );
    post_only_route(
        cfg,
        "/max_draw_down_test",
        strategies::max_draw_down::max_draw_down,
    );
    post_only_route(cfg, "/global_roi_test", strategies::global_roi::global_roi);
    post_only_route(
        cfg,
        "/annual_roi_from_global_roi_test",
        strategies::annual_roi_from_global_roi::annual_roi_from_global_roi,
    );
    post_only_route(
        cfg,
        "/operation_points_table_test",
        strategies::operation_points_table::operation_points_table,
    );
    post_only_route(
        cfg,
        "/operation_points_filter_test",
        strategies::operation_points_filter::operation_points_filter,
    );
    post_only_route(
        cfg,
        "/process_strategy_test",
        strategies::process_strategy::process_strategy,
    );
    post_only_route(
        cfg,
        "/query_long_operation_points_by_mms_test",
        strategies::query_long_operation_points::query_long_operation_points,
    );
    post_only_route(
        cfg,
        "/query_short_operation_points_by_mms_test",
        strategies::query_short_operation_points::query_short_operation_points,
    );
    post_only_route(
        cfg,
        "/query_resampled_points_by_instrument_test",
        strategies::query_resampled_points::query_resampled_points,
    );
    post_only_route(
        cfg,
        "/query_indicators_by_type_test",
        strategies::query_indicators::query_indicators,
    );
    post_only_route(
        cfg,
        "/process_strategies_validator_test",
        strategies::process_strategies_validator::process_strategies_validator,
    );
    post_only_route(
        cfg,
        "/strategy_profitability_test",
        strategies::strategy_profitability::strategy_profitability,
    );
    post_only_route(cfg, "/oscillator_test", signals::oscillator::oscillator);
    post_only_route(cfg, "/crossover_test", signals::crossover::crossover);

    // Indicators
    post_only_route(cfg, "/rsi_test", signals::indicators::rsi::rsi);
}

#[actix_web::main]
async fn main() -> io::Result<()> {
    // Initialize logger
    if let Err(e) = setup_logger() {
        eprintln!("Error initializing logger: {}", e);
        std::process::exit(1);
    }

    let host = std::env::var("HOST").unwrap_or_else(|_| "0.0.0.0:80".into());
    info!("Server starting on {}", &host);

    HttpServer::new(|| App::new().configure(configure_routes))
        .workers(7)
        .bind(&host)?
        .run()
        .await
}
