from config.base import BaseConfig


class ProductionConfig(BaseConfig):
    POSTGRES_HOST = "db-production"
    POSTGRES_PORT = 5432
    POSTGRES_USER = "postgres"
    POSTGRES_PASS = "postgres"
    POSTGRES_DB = "db-production"

    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
