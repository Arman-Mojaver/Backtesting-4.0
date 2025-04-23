"""
Add unique constraint to strategy table.

Revision ID: b7eab2d1c322
Revises: c9fbadc8d783
Create Date: 2025-04-15 09:39:00.117595

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "b7eab2d1c322"
down_revision: str | None = "c9fbadc8d783"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(
        constraint_name="uq_mm_strategy_indicator",
        table_name="strategy",
        columns=("money_management_strategy_id", "indicator_id"),
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("uq_mm_strategy_indicator"),
        "strategy",
        type_="unique",
    )
