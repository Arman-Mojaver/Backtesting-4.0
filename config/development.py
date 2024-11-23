from config.base import BaseConfig


class DevelopmentConfig(BaseConfig):
    POSTGRES_HOST = "db-development"
    POSTGRES_PORT = 54320
    POSTGRES_USER = "postgres"
    POSTGRES_PASS = "postgres"
    POSTGRES_DB = "db-development"

    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
