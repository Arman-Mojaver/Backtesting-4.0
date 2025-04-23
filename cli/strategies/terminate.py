from __future__ import annotations

import click
from celery.app.control import Control, Inspect

from cli.utils import confirm
from config import config  # type: ignore[attr-defined]
from logger import log
from tasks import celery


@click.command("terminate", help="Terminate Create Strategies Task")
def terminate_strategies_task() -> None:
    if config.is_production():
        confirm(
            "You are about to terminate create strategies task in production. "
            "Do you wish to continue?"
        )

    inspect = Inspect(app=celery)
    active_task_ids = [
        task["id"] for tasks in inspect.active().values() for task in tasks
    ]
    if len(active_task_ids) != 1:
        err = f"There should be 1 active task, but there is {len(active_task_ids)}"
        log.info(err)
        raise click.ClickException(err)

    task_id = next(iter(active_task_ids))

    control = Control(app=celery)
    control.purge()
    control.terminate(task_id)

    log.info(f"Terminated task. Task ID: {task_id}")


if __name__ == "__main__":
    terminate_strategies_task()
