import os
from collections.abc import Generator
from copy import deepcopy

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

os.environ["ENVIRONMENT"] = "testing"

from config import config as project_config  # type: ignore[attr-defined]

if not project_config.is_testing():
    err = f"Invalid testing environment: {project_config}"
    raise ValueError(err)


@pytest.fixture(scope="session")
def debug(request) -> bool:
    return request.config.getoption("--d")


@pytest.fixture(scope="session", autouse=True)
def _setup_test_database(*, debug: bool) -> Generator[None, None, None]:
    """Create the test database, runs migrations, and tear it down afterward."""
    if database_exists(project_config.SQLALCHEMY_DATABASE_URI):
        drop_database(project_config.SQLALCHEMY_DATABASE_URI)
    create_database(project_config.SQLALCHEMY_DATABASE_URI)

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    yield

    if not debug:
        drop_database(project_config.SQLALCHEMY_DATABASE_URI)


@pytest.fixture
def session() -> Session:
    """Provide a SQLAlchemy session for tests."""
    engine = create_engine(project_config.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)  # noqa: N806
    session = Session()

    yield session

    session.close()
    engine.dispose()


DATA = {
    "data": {
        "EURUSD": {
            "raw_points_d1": [
                {
                    "close": 1.06981,
                    "datetime": "2023-11-13",
                    "high": 1.0706,
                    "instrument": "EURUSD",
                    "low": 1.06648,
                    "open": 1.06751,
                    "volume": 47554,
                },
                {
                    "close": 1.08782,
                    "datetime": "2023-11-14",
                    "high": 1.08872,
                    "instrument": "EURUSD",
                    "low": 1.06916,
                    "open": 1.06916,
                    "volume": 79728,
                },
            ],
            "raw_points_h1": [
                {
                    "close": 1.06981,
                    "datetime": "2023-11-13 00:00",
                    "high": 1.0706,
                    "instrument": "EURUSD",
                    "low": 1.06648,
                    "open": 1.06751,
                    "volume": 47554,
                },
                {
                    "close": 1.06981,
                    "datetime": "2023-11-13 01:00",
                    "high": 1.0706,
                    "instrument": "EURUSD",
                    "low": 1.06648,
                    "open": 1.06751,
                    "volume": 47554,
                },
                {
                    "close": 1.08782,
                    "datetime": "2023-11-14 00:00",
                    "high": 1.08872,
                    "instrument": "EURUSD",
                    "low": 1.06916,
                    "open": 1.06916,
                    "volume": 79728,
                },
                {
                    "close": 1.08782,
                    "datetime": "2023-11-14 01:00",
                    "high": 1.08872,
                    "instrument": "EURUSD",
                    "low": 1.06916,
                    "open": 1.06916,
                    "volume": 79728,
                },
            ],
        },
        "USDCAD": {
            "raw_points_d1": [
                {
                    "close": 1.06981,
                    "datetime": "2023-11-13",
                    "high": 1.0706,
                    "instrument": "USDCAD",
                    "low": 1.06648,
                    "open": 1.06751,
                    "volume": 47554,
                },
                {
                    "close": 1.08782,
                    "datetime": "2023-11-14",
                    "high": 1.08872,
                    "instrument": "USDCAD",
                    "low": 1.06916,
                    "open": 1.06916,
                    "volume": 79728,
                },
            ],
            "raw_points_h1": [
                {
                    "close": 1.06981,
                    "datetime": "2023-11-13 00:00",
                    "high": 1.0706,
                    "instrument": "USDCAD",
                    "low": 1.06648,
                    "open": 1.06751,
                    "volume": 47554,
                },
                {
                    "close": 1.06981,
                    "datetime": "2023-11-13 01:00",
                    "high": 1.0706,
                    "instrument": "USDCAD",
                    "low": 1.06648,
                    "open": 1.06751,
                    "volume": 47554,
                },
                {
                    "close": 1.08782,
                    "datetime": "2023-11-14 00:00",
                    "high": 1.08872,
                    "instrument": "USDCAD",
                    "low": 1.06916,
                    "open": 1.06916,
                    "volume": 79728,
                },
                {
                    "close": 1.08782,
                    "datetime": "2023-11-14 01:00",
                    "high": 1.08872,
                    "instrument": "USDCAD",
                    "low": 1.06916,
                    "open": 1.06916,
                    "volume": 79728,
                },
            ],
        },
    }
}


@pytest.fixture()
def file_data():
    return deepcopy(DATA)
