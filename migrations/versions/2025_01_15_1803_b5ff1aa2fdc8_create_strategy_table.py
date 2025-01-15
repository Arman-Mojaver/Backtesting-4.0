"""
Create strategy table.

Revision ID: b5ff1aa2fdc8
Revises: d191701b3eb9
Create Date: 2025-01-15 18:03:27.561365

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "b5ff1aa2fdc8"
down_revision: str | None = "d191701b3eb9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "strategy",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("annual_roi", sa.Float(), nullable=False),
        sa.Column("max_draw_down", sa.Float(), nullable=False),
        sa.Column("min_annual_roi", sa.Float(), nullable=False),
        sa.Column("annual_operation_count", sa.Float(), nullable=False),
        sa.Column("money_management_strategy_id", sa.Integer(), nullable=False),
        sa.Column("indicator_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["indicator_id"],
            ["indicator.id"],
            name=op.f("fk_strategy_indicator_id_indicator"),
        ),
        sa.ForeignKeyConstraint(
            ["money_management_strategy_id"],
            ["money_management_strategy.id"],
            name=op.f(
                "fk_strategy_money_management_strategy_id_money_management_strategy"
            ),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_strategy")),
    )


def downgrade() -> None:
    op.drop_table("strategy")
