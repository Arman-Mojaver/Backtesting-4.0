from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, field_validator


class RsiParametersSchema(BaseModel):
    type: Literal["rsi"]
    parameters: dict[str, Any]
    identifier: str

    @field_validator("parameters")
    @classmethod
    def validate_parameters(cls, value: dict[str, Any]) -> dict[str, Any]:
        if "n" not in value:
            err = "Missing required key 'n' in parameters."
            raise ValueError(err)

        if not isinstance(value.get("n"), int) or value.get("n") <= 0:
            err = "'n' must be a non-negative integer."
            raise ValueError(err)

        return value
