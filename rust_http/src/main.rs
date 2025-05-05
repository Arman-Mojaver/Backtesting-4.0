use actix_web::{get, web, App, HttpResponse, HttpServer, Responder};
use serde::Serialize;

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
    web::Json(PingResponse {
        message: "Ping!".into(),
    })
}

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let host = std::env::var("HOST").unwrap_or_else(|_| "0.0.0.0:81".into());
    println!("Server starting on port {}...", &host);

    HttpServer::new(|| {
        App::new()
            .default_service(web::route().to(index))
            .service(ping)
    })
    .workers(7)
    .bind(host)?
    .run()
    .await
}
