from time import sleep

from logger import log
from tasks.celery_app import celery


@celery.task(name="create_strategies_recursively")
def create_strategies_recursively(instrument: str) -> bool:
    log.info(
        f"Created task 'create_strategies_recursively', with instrument: {instrument}"
    )
    sleep(20)
    return True
