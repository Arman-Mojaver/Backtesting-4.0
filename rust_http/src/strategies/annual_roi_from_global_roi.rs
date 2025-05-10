use actix_web::{web, HttpResponse, Responder};
use chrono::NaiveDate;
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct GlobalRoiWithDatesPayload {
    global_roi: f64,
    start_date: NaiveDate,
    end_date: NaiveDate,
}

pub async fn annual_roi_from_global_roi(payload: web::Json<GlobalRoiWithDatesPayload>) -> impl Responder {
    let annual_roi: f64 = get_annual_roi_from_global_roi(payload.global_roi, payload.start_date, payload.end_date);
    HttpResponse::Ok().json(serde_json::json!({ "data": annual_roi }))
}

fn round(value: f64, places: u32) -> f64 {
    let scale = 10_f64.powi(places as i32);
    (value * scale).round() / scale
}

fn get_difference_in_years(start: NaiveDate, end: NaiveDate) -> f64 {
    let days = (end - start).num_days() as f64;
    let years = days.abs() / 365.25;
    round(years, 2)
}

pub fn get_annual_roi_from_global_roi(global_roi: f64, start_date: NaiveDate, end_date: NaiveDate) -> f64 {
    let years = get_difference_in_years(start_date, end_date);
    if years == 0.0 {
        return 0.0;
    }

    let global_accumulated_value = 1.0 + global_roi / 100.0;
    let annual_accumulated_value = global_accumulated_value.powf(1.0 / years);
    let annual_roi = (annual_accumulated_value - 1.0) * 100.0;
    round(annual_roi, 2)
}
