use crate::signals::indicator_values::IndicatorValues;
use crate::strategies::ResampledPointD1;
use serde_json::Value;
use std::str::FromStr;

#[derive(Debug, Clone)]
pub enum IndicatorType {
    RSI,
}

impl FromStr for IndicatorType {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.to_lowercase().as_str() {
            "rsi" => Ok(IndicatorType::RSI),
            other => panic!("Unknown indicator type: {}", other),
        }
    }
}

impl IndicatorType {
    pub fn generate_indicator_values(
        &self,
        resampled_points: &Vec<ResampledPointD1>,
        params: &Value,
    ) -> IndicatorValues {
        match self {
            IndicatorType::RSI => IndicatorValues::OneThreshold(self.get_rsi(
                resampled_points,
                params,
                PriceField::Close,
            )),
        }
    }
}

#[derive(Debug, Clone, Copy)]
pub enum PriceField {
    Open,
    High,
    Low,
    Close,
}

impl PriceField {
    pub fn select(&self, point: &ResampledPointD1) -> f64 {
        match self {
            PriceField::Open => point.open,
            PriceField::High => point.high,
            PriceField::Low => point.low,
            PriceField::Close => point.close,
        }
    }
}
