pub mod annual_operation_count;
pub mod annual_roi_from_global_roi;
pub mod global_roi;
pub mod max_draw_down;
pub mod operation_points_filter;
pub mod operation_points_map;
pub mod process_strategies;
pub mod process_strategy;
pub mod query_long_operation_points;

use anyhow::Result;
use serde::{Deserialize, Serialize};
use sqlx::{FromRow, Pool, Postgres};

#[derive(Debug, Serialize, Deserialize)]
pub struct OperationPointsPayload {
    operation_points: Vec<OperationPoint>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct SignalGroup {
    pub long_signals: Vec<i32>,
    pub short_signals: Vec<i32>,
}

#[derive(Debug, FromRow, Serialize, Deserialize, Clone)]
pub struct OperationPoint {
    instrument: String,
    result: i32,
    tp: i32,
    risk: f64,
    money_management_strategy_id: i32,
    id: i32,
    sl: i32,
    timestamp: i32,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Strategy {
    annual_roi: f64,
    max_draw_down: f64,
    annual_operation_count: f64,
    money_management_strategy_id: i32,
    indicator_id: i32,
}

pub struct OperationPointRepo;

impl OperationPointRepo {
    pub async fn fetch_long_by_mm_strategy(
        pool: &Pool<Postgres>,
        money_management_strategy_id: i32,
    ) -> Result<Vec<OperationPoint>> {
        let records = sqlx::query_as::<_, OperationPoint>(
            r#"
            SELECT
                id,
                instrument,
                result,
                tp,
                sl,
                risk,
                timestamp,
                money_management_strategy_id
            FROM long_operation_point
            WHERE money_management_strategy_id = $1
            ORDER BY id
            "#,
        )
        .bind(money_management_strategy_id)
        .fetch_all(pool)
        .await?;
        Ok(records)
    }
}
