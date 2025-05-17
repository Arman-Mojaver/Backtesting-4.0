use crate::config::DbConfig;
use crate::db::init_pool;
use crate::strategies::{OperationPoint, OperationPointRepo};
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use sqlx::{Pool, Postgres};

#[derive(Debug, Serialize, Deserialize)]
pub struct QueryShortOperationPointsPayload {
    money_management_strategy_id: i32,
}

pub async fn query_short_operation_points(
    payload: web::Json<QueryShortOperationPointsPayload>,
) -> impl Responder {
    let db_config = DbConfig::testing();
    let db_pool = init_pool(db_config).await.expect("DB pool init failed");
    let short_points =
        get_query_short_operation_points(&db_pool, payload.money_management_strategy_id).await;

    HttpResponse::Ok().json(serde_json::json!({ "data": short_points }))
}

pub async fn get_query_short_operation_points(
    db_pool: &Pool<Postgres>,
    money_management_strategy_id: i32,
) -> Vec<OperationPoint> {
    OperationPointRepo::fetch_short_by_mm_strategy(db_pool, money_management_strategy_id)
        .await
        .unwrap()
}
