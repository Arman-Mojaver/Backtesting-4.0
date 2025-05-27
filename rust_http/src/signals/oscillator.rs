use crate::signals::indicator_values::{IndicatorValue, IndicatorValues, OneBuffer};
use crate::strategies::SignalGroup;
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct IndicatorValuesListPayload {
    indicator_value_list: Vec<IndicatorValue>,
}

pub async fn oscillator(payload: web::Json<IndicatorValuesListPayload>) -> impl Responder {
    let indicator_values = IndicatorValues::One(OneBuffer {
        items: payload.indicator_value_list.clone(),
    });

    let signal_group = indicator_values.generate_signals();

    HttpResponse::Ok().json(serde_json::json!({ "data": signal_group }))
}

impl IndicatorValues {
    #[inline]
    pub fn oscillator(&self, buffer: &OneBuffer) -> SignalGroup {
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
            if prev.value < 0.0 && curr.value > 0.0 {
                long_signals.push(curr.timestamp);
            } else if prev.value > 0.0 && curr.value < 0.0 {
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
