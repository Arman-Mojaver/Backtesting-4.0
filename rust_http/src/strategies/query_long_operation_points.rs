use crate::config::DbConfig;
use crate::db::init_pool;
use crate::strategies::{OperationPoint, OperationPointRepo, QueryOperationPointsPayload};
use actix_web::{web, HttpResponse, Responder};
use sqlx::{Pool, Postgres};

pub async fn query_long_operation_points(
    payload: web::Json<QueryOperationPointsPayload>,
) -> impl Responder {
    let db_config = DbConfig::testing();
    let db_pool = init_pool(db_config).await.expect("DB pool init failed");
    let long_points =
        get_query_long_operation_points(&db_pool, payload.money_management_strategy_id).await;

    HttpResponse::Ok().json(serde_json::json!({ "data": long_points }))
}

pub async fn get_query_long_operation_points(
    db_pool: &Pool<Postgres>,
    money_management_strategy_id: i32,
) -> Vec<OperationPoint> {
    OperationPointRepo::fetch_long_by_mm_strategy(db_pool, money_management_strategy_id)
        .await
        .unwrap()
}
