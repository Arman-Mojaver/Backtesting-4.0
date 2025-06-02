from __future__ import annotations

from typing import Any


def get_indicator_data(
    indicator: str,
    instrument: str,
    params: str,
    buffer: str,
) -> list[dict[str, Any]]:
    indicator_map = {}

    try:
        return indicator_map[indicator][instrument][params][buffer]
    except KeyError as exc:
        err = f"Could not find data for: {indicator}, {instrument=}, {params=}, {buffer=}"
        raise KeyError(err) from exc
