import os

from celery import Celery, signals

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0")
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://redis:6379/0"
)
celery.conf.timezone = "UTC"


@signals.setup_logging.connect
def setup_celery_logging(**kwargs) -> None:  # noqa: ANN003
    # Prevent Celery from configuring any logging
    pass
