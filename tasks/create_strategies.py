from database.models import Indicator, MoneyManagementStrategy, ResampledPointD1, Strategy
from database.models.money_management_strategy import MoneyManagementStrategyList
from logger import log
from tasks.celery_app import celery
from views.process_strategies.operation_points_validator import (
    InvalidOperationPointsError,
    OperationPointsValidator,
)


@celery.task(name="create_strategies_recursively")
def create_strategies_recursively(instrument: str) -> bool:
    money_management_strategy_ids = MoneyManagementStrategyList(
        MoneyManagementStrategy.query.all()
    ).get_ids()

    strategy_mm_strategy_ids = Strategy.query.distinct_money_management_strategy_ids()

    ids = money_management_strategy_ids - strategy_mm_strategy_ids
    if not ids:
        log.info("No more unprocessed money management strategies")
        return False

    money_management_strategy_id = next(iter(ids))
    log.info(
        f"Processing Money Management Strategy with ID: {money_management_strategy_id}"
    )
    queried_money_management_strategy = (
        MoneyManagementStrategy.query.from_id(id=money_management_strategy_id)
        .with_operation_points()
        .one()
    )
    queried_resampled_points = ResampledPointD1.query.from_instrument(  # noqa: F841
        instrument=instrument,
    ).all()
    queried_indicators = Indicator.query.all()  # noqa: F841

    try:
        operation_points = OperationPointsValidator(  # noqa: F841
            money_management_strategy_id=money_management_strategy_id,
            long_operation_points=queried_money_management_strategy.long_operation_points,
            short_operation_points=queried_money_management_strategy.short_operation_points,
        ).run()
    except InvalidOperationPointsError as e:
        log.exception(f"Invalid operation points: {e}")
        return False

    log.info("Finished OperationPointsValidator")

    return True
