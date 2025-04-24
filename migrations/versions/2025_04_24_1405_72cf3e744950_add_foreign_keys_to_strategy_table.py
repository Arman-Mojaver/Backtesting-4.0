"""
Add foreign keys to strategy table.

Revision ID: 72cf3e744950
Revises: b7eab2d1c322
Create Date: 2025-04-24 14:05:54.214723

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence


# revision identifiers, used by Alembic.
revision: str = "72cf3e744950"
down_revision: str | None = "b7eab2d1c322"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_foreign_key(
        op.f("fk_strategy_indicator_id_indicator"),
        "strategy",
        "indicator",
        ["indicator_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("fk_strategy_money_management_strategy_id_money_management_strategy"),
        "strategy",
        "money_management_strategy",
        ["money_management_strategy_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_strategy_indicator_id_indicator"), "strategy", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("fk_strategy_money_management_strategy_id_money_management_strategy"),
        "strategy",
        type_="foreignkey",
    )
