use crate::config::DbConfig;
use crate::db::init_pool;
use crate::strategies::{ResampledPointD1, ResampledPointD1Repo};
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use sqlx::{Pool, Postgres};

#[derive(Debug, Serialize, Deserialize)]
pub struct QueryResampledPointsPayload {
    instrument: String,
}

pub async fn query_resampled_points(
    payload: web::Json<QueryResampledPointsPayload>,
) -> impl Responder {
    let db_config = DbConfig::testing();
    let db_pool = init_pool(db_config).await.expect("DB pool init failed");
    let resampled_points = get_query_resampled_points(&db_pool, &payload.instrument).await;

    HttpResponse::Ok().json(serde_json::json!({ "data": resampled_points }))
}

pub async fn get_query_resampled_points(
    db_pool: &Pool<Postgres>,
    instrument: &String,
) -> Vec<ResampledPointD1> {
    ResampledPointD1Repo::fetch_by_instrument(&db_pool, instrument)
        .await
        .unwrap()
}
