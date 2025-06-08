use crate::signals::indicator_types::{IndicatorType, PriceField};
use crate::signals::indicator_values::{IndicatorValue, OneBufferThreshold};
use crate::strategies::{Indicator, ResampledPointD1};
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};
use serde_json::Value;
use std::str::FromStr;

#[derive(Debug, Serialize, Deserialize)]
pub struct RequestPayloadRsi {
    resampled_points: Vec<ResampledPointD1>,
    indicator: Indicator,
}

pub async fn rsi(payload: web::Json<RequestPayloadRsi>) -> impl Responder {
    let indicator: IndicatorType = IndicatorType::from_str("rsi").unwrap();
    let result = indicator
        .generate_indicator_values(&payload.resampled_points, &payload.indicator.parameters);

    HttpResponse::Ok().json(serde_json::json!({ "data": result }))
}

impl IndicatorType {
    pub fn get_rsi(
        &self,
        data: &[ResampledPointD1],
        config: &Value,
        field: PriceField,
    ) -> OneBufferThreshold {
        let period = config
            .get("n")
            .and_then(|v| v.as_u64())
            .expect("Missing or invalid 'n' in config") as usize;

        let diffs: Vec<PriceDiff> = data
            .windows(2)
            .map(|w| {
                let prev = &w[0];
                let cur = &w[1];
                let diff = field.select(cur) - field.select(prev);
                PriceDiff {
                    timestamp: cur.timestamp,
                    diff,
                }
            })
            .collect();

        let indicator_values = diffs.windows(period).map(compute_rsi_point).collect();

        OneBufferThreshold {
            items: indicator_values,
            high_threshold: 70.0,
            low_threshold: 30.0,
        }
    }
}

#[derive(Debug, Serialize, Deserialize, Clone)]
pub struct PriceDiff {
    pub timestamp: i32,
    pub diff: f64,
}

fn compute_rsi_point(window: &[PriceDiff]) -> IndicatorValue {
    let gain: f64 = window.iter().filter(|d| d.diff > 0.0).map(|d| d.diff).sum();
    let loss: f64 = window
        .iter()
        .filter(|d| d.diff < 0.0)
        .map(|d| d.diff.abs())
        .sum();

    let rs = if loss == 0.0 {
        f64::INFINITY
    } else if gain == 0.0 {
        0.0
    } else {
        gain / loss
    };

    let raw_rsi = 100.0 - (100.0 / (1.0 + rs));
    let value = raw_rsi.round();

    let timestamp = window.last().unwrap().timestamp;
    IndicatorValue { timestamp, value }
}
