"""
Add table indices.

Revision ID: 52988e0269c0
Revises: 07c2a22ba073
Create Date: 2025-05-17 15:25:27.001157

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "52988e0269c0"
down_revision: str | None = "07c2a22ba073"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_index(
        "ix_long_operation_point_money_management_strategy_id",
        "long_operation_point",
        ["money_management_strategy_id"],
        unique=False,
    )
    op.create_index(
        "ix_long_operation_point_strategy_strategy_id",
        "long_operation_points_strategies",
        ["strategy_id"],
        unique=False,
    )
    op.create_index(
        "ix_raw_point_d1_instrument", "raw_point_d1", ["instrument"], unique=False
    )
    op.create_index(
        "ix_raw_point_h1_instrument", "raw_point_h1", ["instrument"], unique=False
    )
    op.create_index(
        "ix_resampled_point_d1_instrument",
        "resampled_point_d1",
        ["instrument"],
        unique=False,
    )
    op.create_index(
        "ix_short_operation_point_money_management_strategy_id",
        "short_operation_point",
        ["money_management_strategy_id"],
        unique=False,
    )
    op.create_index(
        "ix_short_operation_point_strategy_strategy_id",
        "short_operation_points_strategies",
        ["strategy_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_short_operation_point_strategy_strategy_id",
        table_name="short_operation_points_strategies",
    )
    op.drop_index(
        "ix_short_operation_point_money_management_strategy_id",
        table_name="short_operation_point",
    )
    op.drop_index("ix_resampled_point_d1_instrument", table_name="resampled_point_d1")
    op.drop_index("ix_raw_point_h1_instrument", table_name="raw_point_h1")
    op.drop_index("ix_raw_point_d1_instrument", table_name="raw_point_d1")
    op.drop_index(
        "ix_long_operation_point_strategy_strategy_id",
        table_name="long_operation_points_strategies",
    )
    op.drop_index(
        "ix_long_operation_point_money_management_strategy_id",
        table_name="long_operation_point",
    )
