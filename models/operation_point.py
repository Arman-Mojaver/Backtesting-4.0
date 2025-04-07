from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from database.models import LongOperationPoint, ShortOperationPoint


@dataclass
class OperationPoints:
    long_operation_points: list[LongOperationPoint]
    short_operation_points: list[ShortOperationPoint]
