import os  # noqa: I001
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from config import config as project_config
from database.models import *  # noqa: F403
from database import Base

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    print(f"ENVIRONMENT={os.getenv("ENVIRONMENT")}")  # noqa: T201
    print(f"SQLALCHEMY_DATABASE_URI={project_config.SQLALCHEMY_DATABASE_URI}")  # noqa: T201

    context.configure(
        url=project_config.SQLALCHEMY_DATABASE_URI,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    print(f"ENVIRONMENT={os.getenv("ENVIRONMENT")}")  # noqa: T201
    print(f"SQLALCHEMY_DATABASE_URI={project_config.SQLALCHEMY_DATABASE_URI}")  # noqa: T201

    alembic_config = config.get_section(config.config_ini_section)
    alembic_config["sqlalchemy.url"] = project_config.SQLALCHEMY_DATABASE_URI

    connectable = engine_from_config(
        alembic_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
