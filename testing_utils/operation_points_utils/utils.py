from __future__ import annotations

from datetime import datetime, timedelta


def generate_weekdays(
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
