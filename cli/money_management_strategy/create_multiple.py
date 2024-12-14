"""
Example.

bt mm_strategies create -t atr -tp 1.1 1.1 -sl 1.4 1.4 -atr 15 15
"""

from __future__ import annotations

import click
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from logger import log
from utils.range_utils import InvalidRangeInputsError
from views.money_management_strategy.create_multiple_view import (
    MoneyManagementStrategyCreateMultipleView,
)


@click.command("create", help="Create multiple MoneyManagementStrategy")
@click.option(
    "-t",
    "--type",
    type=str,
    default="atr",
    required=True,
    help="Money Management Strategy type",
)
@click.option(
    "-tp",
    "--tp_multiplier_range",
    type=click.Tuple([float, float]),
    required=True,
    help="TP Multiplier range",
)
@click.option(
    "-sl",
    "--sl_multiplier_range",
    type=click.Tuple([float, float]),
    required=True,
    help="SL Multiplier range",
)
@click.option(
    "-atr",
    "--atr_parameter_range",
    type=click.Tuple([int, int]),
    required=True,
    help="ATR parameter range",
)
def create_multiple_money_management_strategies(
    type: str,  # noqa: A002
    tp_multiplier_range: tuple[float, float],
    sl_multiplier_range: tuple[float, float],
    atr_parameter_range: tuple[int, int],
) -> None:
    if config.is_production():
        confirm(
            "You are about to create multiple money management strategies in production. "
            "Do you wish to continue?"
        )

    try:
        MoneyManagementStrategyCreateMultipleView(
            type=type,
            tp_multiplier_range=tp_multiplier_range,
            sl_multiplier_range=sl_multiplier_range,
            atr_parameter_range=atr_parameter_range,
        ).run()
    except InvalidRangeInputsError as e:
        err = f"Invalid range input: {e}"
        log.exception("Invalid range input")
        raise click.ClickException(err) from e

    except ValidationError as e:
        err = f"Validation error: {e}"
        log.exception("Validation error")
        raise click.ClickException(err) from e

    except SQLAlchemyError as e:
        err = f"DB error: {e}"
        log.exception("DB error")
        raise click.ClickException(err) from e

    except Exception as e:
        err = f"Unexpected error: {e}"
        log.exception("Unexpected error")
        raise click.ClickException(err) from e

    log.info("Created money management strategies")


if __name__ == "__main__":
    create_multiple_money_management_strategies()
