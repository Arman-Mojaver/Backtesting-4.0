import os
from collections.abc import Generator

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

os.environ["ENVIRONMENT"] = "testing"

from config import config as project_config  # noqa: I001


if not project_config.is_testing():
    err = f"Invalid testing environment: {project_config}"
    raise ValueError(err)


@pytest.fixture(scope="session")
def debug(request) -> bool:  # noqa: ANN001
    return request.config.getoption("--d")


@pytest.fixture(scope="session", autouse=True)
def _setup_test_database(*, debug: bool) -> Generator[None, None, None]:
    """Create the test database, runs migrations, and tear it down afterward."""
    if database_exists(project_config.SQLALCHEMY_DATABASE_URI):  # type: ignore[attr-defined]
        drop_database(project_config.SQLALCHEMY_DATABASE_URI)  # type: ignore[attr-defined]
    create_database(project_config.SQLALCHEMY_DATABASE_URI)  # type: ignore[attr-defined]

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    yield

    if not debug:
        drop_database(project_config.SQLALCHEMY_DATABASE_URI)  # type: ignore[attr-defined]


@pytest.fixture
def session() -> Session:
    """Provide a SQLAlchemy session for tests."""
    engine = create_engine(project_config.SQLALCHEMY_DATABASE_URI)  # type: ignore[attr-defined]
    Session = sessionmaker(bind=engine)  # noqa: N806
    session = Session()

    yield session

    session.close()
    engine.dispose()
