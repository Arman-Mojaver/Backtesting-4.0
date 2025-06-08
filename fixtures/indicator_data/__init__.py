from __future__ import annotations

from typing import Any

from fixtures.indicator_data.rsi import rsi_map


def get_indicator_data(
    indicator: str,
    instrument: str,
    params: str,
    buffer: str,
) -> list[dict[str, Any]]:
    indicator_map = {"rsi": rsi_map}

    try:
        return indicator_map[indicator][instrument][params][buffer]
    except KeyError as exc:
        err = f"Could not find data for: {indicator}, {instrument=}, {params=}, {buffer=}"
        raise KeyError(err) from exc
