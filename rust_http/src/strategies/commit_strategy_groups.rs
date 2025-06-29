use crate::config::DbConfig;
use crate::db::init_pool;
use crate::strategies::process_strategy::StrategyGroup;
use crate::strategies::Strategy;
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use sqlx::{Pool, Postgres, Row, Transaction};

#[derive(Debug, Serialize, Deserialize)]
pub struct CommitStrategyGroupsPayload {
    strategy_groups: Vec<StrategyGroup>,
}

pub async fn commit_strategy_groups(
    payload: web::Json<CommitStrategyGroupsPayload>,
) -> impl Responder {
    let db_config = DbConfig::testing();
    let db_pool = init_pool(db_config).await.expect("DB pool init failed");

    match get_commit_strategy_groups(&db_pool, &payload.strategy_groups).await {
        Ok(strategy_ids) => HttpResponse::Ok().json(serde_json::json!({ "data": strategy_ids })),
        Err(e) => {
            log::error!("Failed to commit strategy groups: {:?}", e);
            HttpResponse::InternalServerError().finish()
        }
    }
}

pub async fn get_commit_strategy_groups(
    db_pool: &Pool<Postgres>,
    strategy_groups: &[StrategyGroup],
) -> Result<Vec<i32>, sqlx::Error> {
    let mut tx: Transaction<'_, Postgres> = db_pool.begin().await?;
    let mut inserted_ids = Vec::with_capacity(strategy_groups.len());

    for sg in strategy_groups {
        let s: &Strategy = &sg.strategy;

        let row = sqlx::query(
            r#"
            INSERT INTO strategy
              (instrument, annual_roi, max_draw_down, annual_operation_count,
               money_management_strategy_id, indicator_id)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id
            "#,
        )
        .bind(&s.instrument)
        .bind(s.annual_roi)
        .bind(s.max_draw_down)
        .bind(s.annual_operation_count)
        .bind(s.money_management_strategy_id)
        .bind(s.indicator_id)
        .fetch_one(&mut *tx)
        .await?;

        let strategy_id: i32 = row.get("id");
        inserted_ids.push(strategy_id);

        for lop_id in &sg.long_operation_point_ids {
            sqlx::query(
                r#"
                INSERT INTO long_operation_points_strategies
                  (long_operation_point_id, strategy_id)
                VALUES ($1, $2)
                "#,
            )
            .bind(lop_id)
            .bind(strategy_id)
            .execute(&mut *tx)
            .await?;
        }

        for sop_id in &sg.short_operation_point_ids {
            sqlx::query(
                r#"
                INSERT INTO short_operation_points_strategies
                  (short_operation_point_id, strategy_id)
                VALUES ($1, $2)
                "#,
            )
            .bind(sop_id)
            .bind(strategy_id)
            .execute(&mut *tx)
            .await?;
        }
    }

    tx.commit().await?;
    Ok(inserted_ids)
}
