from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from itertools import product
from pathlib import Path

from utils.date_utils import string_to_datetime

instruments = ("EURUSD", "USDCAD", "AUDUSD", "AUDCAD")
indicator_names = ("rsi",)
buffers = ("b0",)
params = ("n1", "n2", "n3", "n4")
start_date = "2023-09-11"


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


def generate_indicator_value_data(
    count: int,
    start_date: str | None,
) -> list[tuple[str, float]]:
    start_date = string_to_datetime(start_date) if start_date else datetime.today()  # noqa: DTZ002
    dates = generate_weekdays(start_date=start_date, count=count)

    rows = []
    for d in dates:
        date_str = d.strftime("%Y-%m-%d")
        value = round(random.uniform(0, 100), 2)  # noqa: S311
        rows.append((date_str, value))

    return rows


def create_file(file_path: Path, data: list[tuple[str, float]]) -> None:
    with file_path.open(mode="w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["date", "value"])
        writer.writerows(data)


def main() -> None:
    for instrument, indicator_name, buffer, param in product(
        instruments,
        indicator_names,
        buffers,
        params,
    ):
        file_name = f"{instrument}_{indicator_name}_{buffer}_{param}.csv"
        data = generate_indicator_value_data(60, start_date)
        file_path = Path(str(Path.cwd().parent) + "/indicator_csv_data/" + file_name)
        create_file(file_path, data)


if __name__ == "__main__":
    main()
