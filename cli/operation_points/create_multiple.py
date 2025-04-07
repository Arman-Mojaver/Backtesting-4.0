from __future__ import annotations

import click
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from database import session
from database.handler import DatabaseHandler
from database.models import MoneyManagementStrategy, ResampledPointD1
from exceptions import (
    LargeAtrParameterError,
    NoMoneyManagementStrategiesError,
    NoResampledPointsError,
)
from logger import log
from schemas.instruments_schema import EnabledInstrumentsMismatchError
from views.operation_points_view import OperationPointsCreateMultipleView


@click.command("create", help="Create Operation Points")
def create_operation_points() -> None:
    if config.is_production():
        confirm(
            "You are about to create operation points in production. "
            "Do you wish to continue?"
        )

    resampled_points = ResampledPointD1.query.all()
    money_management_strategies = MoneyManagementStrategy.query.all()

    try:
        operation_points = OperationPointsCreateMultipleView(
            resampled_points,
            money_management_strategies,
        ).run()
    except (
        NoResampledPointsError,
        NoMoneyManagementStrategiesError,
        EnabledInstrumentsMismatchError,
        LargeAtrParameterError,
    ) as e:
        err = f"{e}"
        log.exception(err)
        raise click.ClickException(err) from e

    except ValidationError as e:
        err = f"Validation error: {e}"
        log.exception("Validation error")
        raise click.ClickException(err) from e

    except Exception as e:
        err = f"Unexpected error: {e}"
        log.exception("Unexpected error")
        raise click.ClickException(err) from e

    try:
        DatabaseHandler(session=session).commit_long_operation_points(
            long_operation_points=operation_points.long_operation_points
        )

    except SQLAlchemyError as e:
        err = f"DB error: {e}"
        log.exception("DB error")
        raise click.ClickException(err) from e

    except Exception as e:
        err = f"Unexpected error: {e}"
        log.exception("Unexpected error")
        raise click.ClickException(err) from e

    try:
        DatabaseHandler(session=session).commit_short_operation_points(
            short_operation_points=operation_points.short_operation_points
        )

    except SQLAlchemyError as e:
        err = f"DB error: {e}"
        log.exception("DB error")
        raise click.ClickException(err) from e

    except Exception as e:
        err = f"Unexpected error: {e}"
        log.exception("Unexpected error")
        raise click.ClickException(err) from e

    log.info("Created operation points")


if __name__ == "__main__":
    create_operation_points()
