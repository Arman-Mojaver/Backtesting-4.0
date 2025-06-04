use crate::signals::indicator_values::IndicatorValues;
use crate::strategies::ResampledPointD1;
use serde_json::Value;
use std::str::FromStr;

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
            IndicatorType::RSI => IndicatorValues::One(self.get_rsi(resampled_points, params)),
        }
    }
}
