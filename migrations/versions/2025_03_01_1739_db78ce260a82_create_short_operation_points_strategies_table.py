"""
Create short_operation_points_strategies table.

Revision ID: db78ce260a82
Revises: 9edc66950aec
Create Date: 2025-03-01 17:39:50.690812

"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "db78ce260a82"
down_revision: str | None = "9edc66950aec"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "short_operation_points_strategies",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("short_operation_point_id", sa.Integer(), nullable=False),
        sa.Column("strategy_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["short_operation_point_id"],
            ["short_operation_point.id"],
            name=op.f(
                "fk_short_operation_points_strategies_short_operation_point_id_short_operation_point"
            ),
        ),
        sa.ForeignKeyConstraint(
            ["strategy_id"],
            ["strategy.id"],
            name=op.f("fk_short_operation_points_strategies_strategy_id_strategy"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_short_operation_points_strategies")),
    )


def downgrade() -> None:
    op.drop_table("short_operation_points_strategies")
