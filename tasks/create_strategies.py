import requests

from database import session
from database.models import Indicator, MoneyManagementStrategy, Strategy
from database.models.money_management_strategy import MoneyManagementStrategyList
from logger import log
from tasks.celery_app import celery
from testing_utils.http_utils import parse_response


@celery.task(name="create_strategies_recursively")
def create_strategies_recursively(instrument: str) -> bool:
    money_management_strategy_ids = MoneyManagementStrategyList(
        MoneyManagementStrategy.query.all()
    ).get_ids()

    strategy_mm_strategy_ids = Strategy.query.distinct_money_management_strategy_ids()

    ids = money_management_strategy_ids - strategy_mm_strategy_ids
    if not ids:
        log.info("No more unprocessed money management strategies")
        log.info("Task Output: False")
        return False

    money_management_strategy_id = next(iter(ids))
    log.info(
        f"Processing Money Management Strategy with ID: {money_management_strategy_id}"
    )
    indicator_types = [row[0] for row in session.query(Indicator.type).distinct().all()]
    if len(indicator_types) != 1:
        log.info(
            f"There is more than one indicator type in the database: {indicator_types}"
        )
        log.info("Task Output: False")
        return False

    indicator_type = next(iter(indicator_types))

    data = {
        "instrument": instrument,
        "money_management_strategy_id": money_management_strategy_id,
        "indicator_type": indicator_type,
    }

    log.info("Sending request")
    response = requests.post(
        url="http://host.docker.internal/process_strategies",
        json=data,
        timeout=300,
    )
    log.info("Processing response")
    content = parse_response(response)
    log.info(content)

    log.info("Task Output: True")
    return True
