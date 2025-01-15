"""Import all models here so changes can be detected by alembic."""

from __future__ import annotations

from database.models.indicator import Indicator
from database.models.long_operation_point import LongOperationPoint
from database.models.money_management_strategy import MoneyManagementStrategy
from database.models.raw_point_d1 import RawPointD1
from database.models.raw_point_h1 import RawPointH1
from database.models.resasmpled_point_d1 import ResampledPointD1
from database.models.short_operation_point import ShortOperationPoint
from database.models.strategy import Strategy

__all__: list[str] = [
    "Indicator",
    "LongOperationPoint",
    "MoneyManagementStrategy",
    "RawPointD1",
    "RawPointH1",
    "ResampledPointD1",
    "ShortOperationPoint",
    "Strategy",
]
