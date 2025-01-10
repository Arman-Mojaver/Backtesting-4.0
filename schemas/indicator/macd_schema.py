from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, NonNegativeInt, field_validator


class Parameter(BaseModel):
    n: NonNegativeInt
    price_target: Literal["open", "high", "low", "close"]
    type: Literal["ema", "sma"]


class MacdParametersSchema(BaseModel):
    type: Literal["macd"]
    parameters: dict[str, Parameter]
    identifier: str

    @field_validator("parameters")
    @classmethod
    def validate_parameters(cls, value: dict[str, Parameter]) -> dict[str, Parameter]:
        required_keys = {"fast", "slow"}
        if not required_keys.issubset(value.keys()):
            err = f"Parameters must include the keys: {required_keys}"
            raise ValueError(err)

        return value
