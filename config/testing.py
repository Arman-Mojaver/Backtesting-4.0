from config.base import BaseConfig


class TestingConfig(BaseConfig):
    POSTGRES_HOST = "db-testing"
    POSTGRES_PORT = 54321
    POSTGRES_USER = "postgres"
    POSTGRES_PASS = "postgres"
    POSTGRES_DB = "db-testing"

    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
