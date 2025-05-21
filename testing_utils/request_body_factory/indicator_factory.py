from __future__ import annotations

from database.models.indicator import Indicator


def generate_rsi_indicators(count: int) -> list[Indicator]:
    return [
        Indicator(
            id=1000 + i,
            type="rsi",
            parameters={"n": 8 + i},
            identifier=f"rsi.{8 + i}",
        )
        for i in range(count)
    ]


def generate_macd_indicators(count: int) -> list[Indicator]:
    return [
        Indicator(
            id=2000 + i,
            type="macd",
            parameters={
                "slow": {"type": "sma", "n": 8 + i, "price_target": "close"},
                "fast": {"type": "ema", "n": 5 + i, "price_target": "close"},
            },
            identifier=f"macd.sma-{8 + 1}-close,ema-{5 + i}-close",
        )
        for i in range(count)
    ]
