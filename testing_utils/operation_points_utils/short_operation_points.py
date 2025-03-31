from __future__ import annotations

import functools
import random
from datetime import datetime

from database.models import ShortOperationPoint
from testing_utils.operation_points_utils.utils import generate_weekdays


def generate_random_short_operation_point(
    money_management_strategy_id: int,
    instrument: str,
    date: datetime.date,
) -> ShortOperationPoint:
    result = random.choice(list(range(30, 71)) + list(range(-70, -29)))  # noqa: S311
    short_balance = [random.randint(-20, 20) for _ in range(random.randint(2, 10))]  # noqa: S311

    if result > 0:
        tp = result
        sl = random.choice(list(range(30, 71)))  # noqa: S311
        short_balance.append(result + random.randint(1, 15))  # noqa: S311
    else:
        tp = random.choice(list(range(30, 71)))  # noqa: S311
        sl = -result
        short_balance.append(result - random.randint(1, 15))  # noqa: S311

    return ShortOperationPoint(
        instrument=instrument,
        datetime=date,
        result=result,
        tp=tp,
        sl=sl,
        short_balance=short_balance,
        risk=0.02,
        money_management_strategy_id=money_management_strategy_id,
    )


@functools.lru_cache
def generate_random_short_operation_points(
    money_management_strategy_id: int,
    instrument: str,
    start_date: str,
    count: int | None = None,
    end_date: str | None = None,
) -> list[ShortOperationPoint]:
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()  # noqa: DTZ007
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()  # noqa: DTZ007
    dates = generate_weekdays(start_date=start_date, end_date=end_date, count=count)

    return [
        generate_random_short_operation_point(
            money_management_strategy_id=money_management_strategy_id,
            instrument=instrument,
            date=date,
        )
        for date in dates
    ]
