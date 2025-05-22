use crate::strategies::Strategy;
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct StrategyProfitabilityParameters {
    global_min_annual_operation_count: f64,
    global_max_max_draw_down: f64,
    global_min_annual_roi: f64,
}

impl StrategyProfitabilityParameters {
    fn is_profitable(&self, s: &Strategy) -> bool {
        s.annual_operation_count >= self.global_min_annual_operation_count
            && s.max_draw_down <= self.global_max_max_draw_down
            && s.annual_roi >= self.global_min_annual_roi
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct StrategyProfitabilityPayload {
    strategies: Vec<Strategy>,
    strategy_profitability_parameters: StrategyProfitabilityParameters,
}

pub async fn strategy_profitability(
    payload: web::Json<StrategyProfitabilityPayload>,
) -> impl Responder {
    let StrategyProfitabilityPayload {
        strategies,
        strategy_profitability_parameters: params,
    } = payload.into_inner();

    let profitable_strategies = get_strategy_profitability(strategies, params);

    HttpResponse::Ok().json(serde_json::json!({ "data": profitable_strategies }))
}

pub fn get_strategy_profitability(
    strategies: Vec<Strategy>,
    params: StrategyProfitabilityParameters,
) -> Vec<Strategy> {
    strategies
        .into_iter()
        .filter(|s| params.is_profitable(s))
        .collect()
}
