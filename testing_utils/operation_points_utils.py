from __future__ import annotations

import random
from datetime import datetime, timedelta

from database.models import LongOperationPoint, ShortOperationPoint


def _generate_weekdays(
    start_date: datetime.date,
    end_date: datetime.date | None = None,
    count: int | None = None,
) -> list[datetime.date]:
    if count and end_date:
        err = "Pass either 'count' or 'end_date', not both."
        raise ValueError(err)

    if not (count or end_date):
        err = "Pass either 'count' or 'end_date'."
        raise ValueError(err)

    dates = []
    current_date = start_date

    if count:
        while len(dates) < count:
            if current_date.weekday() < 5:  # Exclude weekends  # noqa: PLR2004
                dates.append(current_date)
            current_date += timedelta(days=1)
    else:
        while current_date <= end_date:
            if current_date.weekday() < 5:  # Exclude weekends  # noqa: PLR2004
                dates.append(current_date)
            current_date += timedelta(days=1)

    return dates


# Long operation points


def generate_random_long_operation_point(
    money_management_strategy_id: int,
    instrument: str,
    date: datetime.date,
) -> LongOperationPoint:
    result = random.choice(list(range(30, 71)) + list(range(-70, -29)))  # noqa: S311
    long_balance = [random.randint(-20, 20) for _ in range(random.randint(2, 10))]  # noqa: S311

    if result > 0:
        tp = result
        sl = random.choice(list(range(30, 71)))  # noqa: S311
        long_balance.append(result + random.randint(1, 15))  # noqa: S311
    else:
        tp = random.choice(list(range(30, 71)))  # noqa: S311
        sl = -result
        long_balance.append(result - random.randint(1, 15))  # noqa: S311

    return LongOperationPoint(
        instrument=instrument,
        datetime=date,
        result=result,
        tp=tp,
        sl=sl,
        long_balance=long_balance,
        risk=0.02,
        money_management_strategy_id=money_management_strategy_id,
    )


def generate_random_long_operation_points(
    money_management_strategy_id: int,
    instrument: str,
    start_date: str,
    count: int | None = None,
    end_date: str | None = None,
) -> list[LongOperationPoint]:
    """
    # noqa: D401
    This generator excludes weekends, so if the start_date is a Saturday or a Sunday
    the first generated day will be the next Monday. This may lead to unexpected behaviour
    when generating mismatched dates that are mismatched on Saturdays and Sundays.
    To avoid this, the best start dates are between Tuesday and Thursday.
    """
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()  # noqa: DTZ007
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()  # noqa: DTZ007
    dates = _generate_weekdays(start_date=start_date, end_date=end_date, count=count)

    return [
        generate_random_long_operation_point(
            money_management_strategy_id=money_management_strategy_id,
            instrument=instrument,
            date=date,
        )
        for date in dates
    ]


# Short operation points


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
    dates = _generate_weekdays(start_date=start_date, end_date=end_date, count=count)

    return [
        generate_random_short_operation_point(
            money_management_strategy_id=money_management_strategy_id,
            instrument=instrument,
            date=date,
        )
        for date in dates
    ]
