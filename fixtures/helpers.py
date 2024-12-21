from __future__ import annotations

from typing import Any


def generate_identifier(data: dict[str, Any]) -> str:
    return (
        f'{data["type"]}-{data["tp_multiplier"]}-'
        f'{data["sl_multiplier"]}-{data["parameters"]["atr_parameter"]}'
    )
