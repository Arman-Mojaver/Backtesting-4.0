use crate::config::DbConfig;
use crate::db::init_pool;
use crate::strategies::{Indicator, IndicatorRepo};
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use sqlx::{Pool, Postgres};

#[derive(Debug, Serialize, Deserialize)]
pub struct QueryIndicatorsPayload {
    type_: String,
}

pub async fn query_indicators(payload: web::Json<QueryIndicatorsPayload>) -> impl Responder {
    let db_config = DbConfig::testing();
    let db_pool = init_pool(db_config).await.expect("DB pool init failed");
    let indicators = get_query_indicators(&db_pool, &payload.type_).await;
    HttpResponse::Ok().json(serde_json::json!({ "data": indicators }))
}

pub async fn get_query_indicators(db_pool: &Pool<Postgres>, type_: &String) -> Vec<Indicator> {
    IndicatorRepo::fetch_by_type(&db_pool, type_).await.unwrap()
}
