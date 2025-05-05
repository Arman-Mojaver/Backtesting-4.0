use actix_web::{App, HttpServer};
use chrono::Local;
use fern::colors::{Color, ColoredLevelConfig};
use log::info;
use std::io;

mod routes;

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

    HttpServer::new(|| App::new().configure(routes::configure_routes))
        .workers(7)
        .bind(&host)?
        .run()
        .await
}
