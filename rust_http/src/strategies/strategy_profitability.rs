use crate::strategies::Strategy;
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct StrategyProfitabilityParameters {
    annual_operation_count: f64,
    max_draw_down: f64,
    annual_roi: f64,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct StrategyProfitabilityPayload {
    strategies: Vec<Strategy>,
    strategy_profitability_parameters: StrategyProfitabilityParameters,
}

pub async fn strategy_profitability(
    payload: web::Json<StrategyProfitabilityPayload>,
) -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "data": [] }))
}

pub fn get_strategy_profitability() -> i32 {
    0
}
