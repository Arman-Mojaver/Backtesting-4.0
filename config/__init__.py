import os

from config.base import BaseConfig
from config.development import DevelopmentConfig
from config.production import ProductionConfig
from config.testing import TestingConfig

ENABLED_ENVIRONMENTS = ["production", "development", "testing"]
CONFIG_MAPPER = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}


def get_environment() -> str:
    environment = os.environ.get("ENVIRONMENT", "development")

    if environment not in ENABLED_ENVIRONMENTS:
        err = f"Invalid environment: {environment}"
        raise ValueError(err)

    return environment


def get_config() -> BaseConfig:
    environment = get_environment()
    config_class = CONFIG_MAPPER[environment]()
    config_class.ENVIRONMENT = environment
    return config_class


config: BaseConfig = get_config()


__all__ = ["config", "get_config"]
