from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from itertools import product
from pathlib import Path

instruments = ("EURUSD", "USDCAD", "AUDUSD", "AUDCAD")
indicator_names = ("rsi",)
buffers = ("b0", "b1")
params = ("p1", "q1", "p2", "q2")


def generate_indicator_value_data(count: int) -> list[tuple[str, float]]:
    start_date = datetime.today()  # noqa: DTZ002
    rows = []

    for i in range(count):
        date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        value = round(random.uniform(0, 100), 2)  # noqa: S311
        rows.append((date, value))

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
        data = generate_indicator_value_data(100)
        file_path = Path(str(Path.cwd().parent) + "/indicator_data/" + file_name)
        create_file(file_path, data)


if __name__ == "__main__":
    main()
