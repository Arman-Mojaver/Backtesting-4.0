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
    let indicator_values = IndicatorValues::OneThreshold(OneBufferThreshold {
        items: payload.indicator_value_list.clone(),
        high_threshold: payload.high_threshold.clone(),
        low_threshold: payload.low_threshold.clone(),
    });

    let signal_group = indicator_values.generate_signals();
    HttpResponse::Ok().json(serde_json::json!({ "data": signal_group }))
}

impl IndicatorValues {
    #[inline]
    pub fn thresholds(&self, buffer: &OneBufferThreshold) -> SignalGroup {
        let values = &buffer.items;
        let n = values.len();

        let mut long_signals = Vec::with_capacity(n / 2);
        let mut short_signals = Vec::with_capacity(n / 2);

        if n == 0 {
            return SignalGroup {
                long_signals,
                short_signals,
            };
        }

        let mut prev = &values[0];
        for curr in &values[1..] {
            if prev.value < buffer.low_threshold && curr.value > buffer.low_threshold {
                long_signals.push(curr.timestamp);
            } else if prev.value > buffer.high_threshold && curr.value < buffer.high_threshold {
                short_signals.push(curr.timestamp);
            }
            prev = curr;
        }

        SignalGroup {
            long_signals,
            short_signals,
        }
    }
}
