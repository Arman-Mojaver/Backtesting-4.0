from __future__ import annotations

import random
from typing import Any


def generate_random_strategy_data() -> dict[str, Any]:
    annual_roi = round(random.uniform(-0.2, 0.5) * 100, 2)  # noqa: S311
    max_draw_down = round(random.uniform(0.05, 0.4) * 100, 2)  # noqa: S311
    annual_operation_count = random.randint(10, 20)  # noqa: S311

    return {
        "instrument": "EURUSD",
        "annual_roi": annual_roi,
        "max_draw_down": max_draw_down,
        "annual_operation_count": annual_operation_count,
    }
