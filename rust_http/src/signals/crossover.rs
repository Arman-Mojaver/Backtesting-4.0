use crate::signals::indicator_values::{IndicatorValue, IndicatorValues, OneBuffer, TwoBuffers};
use crate::strategies::SignalGroup;
use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct IndicatorValuesTwoListsPayload {
    upcross_long_buffer: Vec<IndicatorValue>,
    upcross_short_buffer: Vec<IndicatorValue>,
}

pub async fn crossover(payload: web::Json<IndicatorValuesTwoListsPayload>) -> impl Responder {
    let indicator_values = IndicatorValues::Two(TwoBuffers {
        upcross_long_buffer: payload.upcross_long_buffer.clone(),
        upcross_short_buffer: payload.upcross_short_buffer.clone(),
    });
    let signal_group = indicator_values.generate_signals();
    HttpResponse::Ok().json(serde_json::json!({ "data": signal_group }))
}

impl IndicatorValues {
    pub fn crossover(&self, buffers: &TwoBuffers) -> SignalGroup {
        let diff_buffer: Vec<IndicatorValue> = buffers
            .upcross_long_buffer
            .iter()
            .zip(buffers.upcross_short_buffer.iter())
            .map(|(long, short)| IndicatorValue {
                timestamp: long.timestamp,
                value: long.value - short.value,
            })
            .collect();

        self.oscillator(&OneBuffer { items: diff_buffer })
    }
}
