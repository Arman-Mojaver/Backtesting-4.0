use crate::signals::indicator_types::IndicatorType;
use crate::signals::indicator_values::OneBuffer;
use crate::strategies::ResampledPointD1;
use actix_web::{web, HttpResponse, Responder};
use serde::Deserialize;
use serde_json::Value;

#[derive(Debug, Deserialize)]
pub struct RequestPayloadRsi {}

pub async fn rsi(_request_body: web::Json<RequestPayloadRsi>) -> impl Responder {
    HttpResponse::Ok().json(serde_json::json!({ "data": [] }))
}

impl IndicatorType {
    pub fn get_rsi(&self, resampled_points: &Vec<ResampledPointD1>, params: &Value) -> OneBuffer {
        OneBuffer { items: vec![] }
    }
}
