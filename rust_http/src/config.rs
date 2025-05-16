use std::{env, str::FromStr};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Environment {
    Production,
    Development,
    Testing,
}

impl Environment {
    pub fn current() -> Self {
        env::var("ENVIRONMENT")
            .ok()
            .and_then(|s| s.parse().ok())
            .unwrap_or(Environment::Development)
    }
}

impl FromStr for Environment {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match &*s.to_lowercase() {
            "production" => Ok(Environment::Production),
            "development" => Ok(Environment::Development),
            "testing" => Ok(Environment::Testing),
            _ => Err(()),
        }
    }
}

#[derive(Debug)]
pub struct DbConfig {
    pub host: String,
    pub port: u16,
    pub user: String,
    pub password: String,
    pub database: String,
}

impl DbConfig {
    pub fn production() -> Self {
        DbConfig {
            host: "db-production".into(),
            port: 5432,
            user: "postgres".into(),
            password: "postgres".into(),
            database: "db-production".into(),
        }
    }

    pub fn development() -> Self {
        DbConfig {
            host: "db-development".into(),
            port: 54320,
            user: "postgres".into(),
            password: "postgres".into(),
            database: "db-development".into(),
        }
    }

    pub fn testing() -> Self {
        DbConfig {
            host: "db-testing".into(),
            port: 54321,
            user: "postgres".into(),
            password: "postgres".into(),
            database: "db-testing".into(),
        }
    }

    pub fn from_env() -> Self {
        match Environment::current() {
            Environment::Production => DbConfig::production(),
            Environment::Development => DbConfig::development(),
            Environment::Testing => DbConfig::testing(),
        }
    }

    pub fn url(&self) -> String {
        format!(
            "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}",
            user = self.user,
            password = self.password,
            host = self.host,
            port = self.port,
            database = self.database,
        )
    }
}
