use crate::signals::indicator_values::{IndicatorValue, IndicatorValues, OneBufferThreshold};
use crate::strategies::SignalGroup;
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct ThresholdsPayload {
    indicator_value_list: Vec<IndicatorValue>,
    high_threshold: f64,
    low_threshold: f64,
}

pub async fn thresholds(payload: web::Json<ThresholdsPayload>) -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "data": [] }))
}

impl IndicatorValues {
    pub fn thresholds(&self, buffer: &OneBufferThreshold) -> SignalGroup {
        SignalGroup {
            long_signals: Vec::new(),
            short_signals: Vec::new(),
        }
    }
}
