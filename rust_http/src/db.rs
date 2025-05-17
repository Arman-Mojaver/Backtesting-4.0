use crate::config::DbConfig;
use sqlx::{postgres::PgPoolOptions, Pool, Postgres, Result};

pub async fn init_pool(db_config: DbConfig) -> Result<Pool<Postgres>> {
    let url = db_config.url();
    let pool = PgPoolOptions::new()
        .max_connections(1)
        .connect(&url)
        .await?;
    Ok(pool)
}
