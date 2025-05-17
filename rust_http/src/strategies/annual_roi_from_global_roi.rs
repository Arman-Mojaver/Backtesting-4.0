use actix_web::{web, HttpResponse, Responder};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct GlobalRoiWithTimestampsPayload {
    global_roi: f64,
    start_date: i32,
    end_date: i32,
}

pub async fn annual_roi_from_global_roi(
    payload: web::Json<GlobalRoiWithTimestampsPayload>,
) -> impl Responder {
    let annual_roi =
        get_annual_roi_from_global_roi(payload.global_roi, payload.start_date, payload.end_date);
    HttpResponse::Ok().json(serde_json::json!({ "data": annual_roi }))
}

fn round(value: f64, places: i32) -> f64 {
    let scale = 10_f64.powi(places as i32);
    (value * scale).round() / scale
}

fn get_difference_in_years(start: i32, end: i32) -> f64 {
    let seconds = (end.max(start) - start.min(end)) as f64;
    let years = seconds / (365.25 * 24.0 * 60.0 * 60.0);
    round(years, 2)
}

pub fn get_annual_roi_from_global_roi(global_roi: f64, start_date: i32, end_date: i32) -> f64 {
    let years = get_difference_in_years(start_date, end_date);
    if years == 0.0 {
        return 0.0;
    }

    let global_accumulated_value = 1.0 + global_roi / 100.0;
    let annual_accumulated_value = global_accumulated_value.powf(1.0 / years);
    let annual_roi = (annual_accumulated_value - 1.0) * 100.0;
    round(annual_roi, 2)
}
