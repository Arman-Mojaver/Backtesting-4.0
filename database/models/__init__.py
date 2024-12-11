"""Import all models here so changes can be detected by alembic."""

from __future__ import annotations

from database.models.money_management_strategy import MoneyManagementStrategy
from database.models.raw_point_d1 import RawPointD1
from database.models.raw_point_h1 import RawPointH1
from database.models.resasmpled_point_d1 import ResampledPointD1

__all__: list[str] = [
    "MoneyManagementStrategy",
    "RawPointD1",
    "RawPointH1",
    "ResampledPointD1",
]
