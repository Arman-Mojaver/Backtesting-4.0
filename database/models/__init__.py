"""Import all models here so changes can be detected by alembic."""

from __future__ import annotations

from database.models.raw_point_d1 import RawPointD1

__all__: list[str] = ["RawPointD1"]
