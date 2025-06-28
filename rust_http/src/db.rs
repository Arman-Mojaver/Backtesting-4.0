use crate::config::DbConfig;
use sqlx::{postgres::PgPoolOptions, Pool, Postgres, Result};

pub async fn init_pool(db_config: DbConfig) -> Result<Pool<Postgres>> {
    let url = db_config.url();
    let pool = PgPoolOptions::new()
        .min_connections(6)
        .max_connections(6)
        .connect(&url)
        .await?;
    Ok(pool)
}
