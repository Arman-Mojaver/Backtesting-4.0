from __future__ import annotations

import functools
import random
from datetime import datetime

from database.models import ShortOperationPoint
from testing_utils.operation_points_utils.utils import generate_weekdays
from utils.date_utils import datetime_to_string, string_to_datetime

SHORT_ID_GAP = 6300


def generate_random_short_operation_point(
    money_management_strategy_id: int,
    instrument: str,
    date: str,
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
        datetime=string_to_datetime(date).date(),
        result=result,
        tp=tp,
        sl=sl,
        short_balance=short_balance,
        risk=0.02,
        money_management_strategy_id=money_management_strategy_id,
        timestamp=int(string_to_datetime(date).timestamp()),
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
    str_dates = [datetime_to_string(date) for date in dates]

    short_operation_points = [
        generate_random_short_operation_point(
            money_management_strategy_id=money_management_strategy_id,
            instrument=instrument,
            date=date,
        )
        for date in str_dates
    ]

    for index, short_operation_point in enumerate(short_operation_points):
        short_operation_point.id = index + SHORT_ID_GAP

    return short_operation_points
