"""
Create long_operation_points_strategies table.

Revision ID: 9edc66950aec
Revises: b5ff1aa2fdc8
Create Date: 2025-03-01 16:48:24.124009

"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9edc66950aec"
down_revision: str | None = "b5ff1aa2fdc8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "long_operation_points_strategies",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("long_operation_point_id", sa.Integer(), nullable=False),
        sa.Column("strategy_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["long_operation_point_id"],
            ["long_operation_point.id"],
            name=op.f(
                "fk_long_operation_points_strategies_long_operation_point_id_long_operation_point"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["strategy_id"],
            ["strategy.id"],
            name=op.f("fk_long_operation_points_strategies_strategy_id_strategy"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_long_operation_points_strategies")),
    )


def downgrade() -> None:
    op.drop_table("long_operation_points_strategies")
