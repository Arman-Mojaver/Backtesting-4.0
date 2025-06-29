use crate::strategies::process_strategy::StrategyGroup;
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct CommitStrategyGroupsPayload {
    strategy_groups: Vec<StrategyGroup>,
}

pub async fn commit_strategy_groups(
    payload: web::Json<CommitStrategyGroupsPayload>,
) -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "data": [] }))
}

pub fn get_commit_strategy_groups() -> i32 {
    0
}
