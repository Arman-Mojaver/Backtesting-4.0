pub mod annual_operation_count;
pub mod annual_roi_from_global_roi;
pub mod global_roi;
pub mod max_draw_down;
pub mod operation_points_filter;
pub mod operation_points_table;
pub mod process_strategies;
pub mod process_strategies_from_signals;
pub mod process_strategies_test;
pub mod process_strategies_validator;
pub mod process_strategy;
pub mod query_indicators;
pub mod query_long_operation_points;
pub mod query_resampled_points;
pub mod query_short_operation_points;
pub mod strategy_profitability;

use anyhow::Result;
use serde::{Deserialize, Serialize};
use serde_json::Value;
use sqlx::types::Json;
use sqlx::{FromRow, Pool, Postgres};

#[derive(Debug, Serialize, Deserialize)]
pub struct OperationPointsPayload {
    operation_points: Vec<OperationPoint>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct QueryOperationPointsPayload {
    money_management_strategy_id: i32,
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

#[derive(Debug, Serialize, Deserialize, Clone)]
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

    pub async fn fetch_short_by_mm_strategy(
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
            FROM short_operation_point
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

#[derive(Debug, FromRow, Serialize, Deserialize, Clone)]
pub struct ResampledPointD1 {
    pub id: i32,
    pub instrument: String,
    pub open: f64,
    pub high: f64,
    pub low: f64,
    pub close: f64,
    pub volume: i32,
    pub timestamp: i32,
}

pub struct ResampledPointD1Repo;

impl ResampledPointD1Repo {
    pub async fn fetch_by_instrument(
        pool: &Pool<Postgres>,
        instrument: &String,
    ) -> Result<Vec<ResampledPointD1>> {
        let records = sqlx::query_as::<_, ResampledPointD1>(
            "SELECT id, instrument, open, high, low, close, volume, timestamp
             FROM resampled_point_d1
             WHERE instrument = $1
             ORDER BY timestamp",
        )
        .bind(instrument)
        .fetch_all(pool)
        .await?;

        Ok(records)
    }
}

#[derive(Debug, Serialize, Deserialize, sqlx::FromRow, Clone)]
pub struct Indicator {
    pub id: i32,
    #[serde(rename = "type")]
    pub r#type: String,
    pub parameters: Json<Value>,
    pub identifier: String,
}

pub struct IndicatorRepo;
impl IndicatorRepo {
    pub async fn fetch_by_type(pool: &Pool<Postgres>, type_: &String) -> Result<Vec<Indicator>> {
        let records = sqlx::query_as::<_, Indicator>(
            "SELECT id, type, parameters, identifier FROM indicator WHERE type = $1",
        )
        .bind(type_)
        .fetch_all(pool)
        .await?;

        Ok(records)
    }
}
