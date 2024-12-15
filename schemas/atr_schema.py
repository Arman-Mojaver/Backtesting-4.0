from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, computed_field


class AtrParameter(BaseModel):
    atr_parameter: int


class AtrSchema(BaseModel):
    type: Literal["atr"]
    tp_multiplier: float = Field(gt=0)
    sl_multiplier: float = Field(gt=0)
    parameters: AtrParameter

    @computed_field  # type: ignore[prop-decorator]
    @property
    def identifier(self) -> str:
        return (
            f"{self.type}-{self.tp_multiplier}-"
            f"{self.sl_multiplier}-{self.parameters.atr_parameter}"
        )
