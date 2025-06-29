use crate::config::DbConfig;
use crate::db::init_pool;
use crate::strategies::process_strategy::StrategyGroup;
use actix_web::{web, HttpResponse, Responder};
use futures::{stream, StreamExt};
use log::info;
use serde::{Deserialize, Serialize};
use sqlx::{Pool, Postgres, Row, Transaction};
use std::time::Instant;

#[derive(Debug, Serialize, Deserialize)]
pub struct CommitStrategyGroupsPayload {
    strategy_groups: Vec<StrategyGroup>,
}

pub async fn commit_strategy_groups(
    payload: web::Json<CommitStrategyGroupsPayload>,
) -> impl Responder {
    let db_config = DbConfig::testing();
    let db_pool = init_pool(db_config).await.expect("DB pool init failed");

    let start = Instant::now();
    info!("/commit_strategy_groups. Starting");

    let response = match get_commit_strategy_groups(&db_pool, &payload.strategy_groups).await {
        Ok(ids) => HttpResponse::Ok().json(serde_json::json!({ "data": ids })),
        Err(e) => {
            log::error!("Failed to commit strategy groups: {:?}", e);
            HttpResponse::InternalServerError().finish()
        }
    };

    let elapsed = start.elapsed();
    info!("Finished /commit_strategy_groups in {:?}", elapsed);

    response
}

async fn get_commit_strategy_groups(
    db_pool: &Pool<Postgres>,
    strategy_groups: &[StrategyGroup],
) -> Result<Vec<i32>, sqlx::Error> {
    const CONCURRENCY: usize = 16;

    let tasks = stream::iter(strategy_groups.iter().enumerate())
        .map(|(idx, sg)| {
            let pool = db_pool.clone();
            async move {
                let row = sqlx::query(
                    r#"
                    INSERT INTO strategy
                      (instrument, annual_roi, max_draw_down, annual_operation_count,
                       money_management_strategy_id, indicator_id)
                    VALUES ($1, $2, $3, $4, $5, $6)
                    RETURNING id
                    "#,
                )
                .bind(&sg.strategy.instrument)
                .bind(sg.strategy.annual_roi)
                .bind(sg.strategy.max_draw_down)
                .bind(sg.strategy.annual_operation_count)
                .bind(sg.strategy.money_management_strategy_id)
                .bind(sg.strategy.indicator_id)
                .fetch_one(&pool)
                .await?;
                let strategy_id: i32 = row.get("id");

                if !sg.long_operation_point_ids.is_empty() {
                    sqlx::query(
                        r#"
                        INSERT INTO long_operation_points_strategies
                          (long_operation_point_id, strategy_id)
                        SELECT UNNEST($1::int[]), $2
                        "#,
                    )
                    .bind(&sg.long_operation_point_ids)
                    .bind(strategy_id)
                    .execute(&pool)
                    .await?;
                }

                if !sg.short_operation_point_ids.is_empty() {
                    sqlx::query(
                        r#"
                        INSERT INTO short_operation_points_strategies
                          (short_operation_point_id, strategy_id)
                        SELECT UNNEST($1::int[]), $2
                        "#,
                    )
                    .bind(&sg.short_operation_point_ids)
                    .bind(strategy_id)
                    .execute(&pool)
                    .await?;
                }

                Ok::<_, sqlx::Error>((idx, strategy_id))
            }
        })
        .buffer_unordered(CONCURRENCY);

    let mut ids = vec![0; strategy_groups.len()];
    futures::pin_mut!(tasks);
    while let Some(res) = tasks.next().await {
        let (idx, id) = res?;
        ids[idx] = id;
    }

    Ok(ids)
}
