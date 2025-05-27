use crate::strategies::SignalGroup;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct IndicatorValue {
    pub timestamp: i32,
    pub value: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OneBuffer {
    pub items: Vec<IndicatorValue>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TwoBuffers {
    pub upcross_long_buffer: Vec<IndicatorValue>,
    pub upcross_short_buffer: Vec<IndicatorValue>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum IndicatorValues {
    One(OneBuffer),
    Two(TwoBuffers),
}

impl IndicatorValues {
    pub fn generate_signals(&self) -> SignalGroup {
        match self {
            IndicatorValues::One(buffer) => self.oscillator(buffer),
            IndicatorValues::Two(buffers) => self.crossover(buffers),
        }
    }
}
