"""
Remove foreign keys from strategy, short_operation_points_strategies,
long_operation_points_strategies tables.

Revision ID: c9fbadc8d783
Revises: 4b559a42f5ca
Create Date: 2025-04-03 08:12:40.172073

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "c9fbadc8d783"
down_revision: str | None = "4b559a42f5ca"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_constraint(
        "fk_long_operation_points_strategies_long_operation_poin_38e8",
        "long_operation_points_strategies",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_long_operation_points_strategies_strategy_id_strategy",
        "long_operation_points_strategies",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_short_operation_points_strategies_strategy_id_strategy",
        "short_operation_points_strategies",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_short_operation_points_strategies_short_operation_po_0c0c",
        "short_operation_points_strategies",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_strategy_indicator_id_indicator", "strategy", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_strategy_money_management_strategy_id_money_manageme_2d58",
        "strategy",
        type_="foreignkey",
    )


def downgrade() -> None:
    op.create_foreign_key(
        "fk_strategy_money_management_strategy_id_money_manageme_2d58",
        "strategy",
        "money_management_strategy",
        ["money_management_strategy_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_strategy_indicator_id_indicator",
        "strategy",
        "indicator",
        ["indicator_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_short_operation_points_strategies_short_operation_po_0c0c",
        "short_operation_points_strategies",
        "short_operation_point",
        ["short_operation_point_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_short_operation_points_strategies_strategy_id_strategy",
        "short_operation_points_strategies",
        "strategy",
        ["strategy_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_long_operation_points_strategies_strategy_id_strategy",
        "long_operation_points_strategies",
        "strategy",
        ["strategy_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_long_operation_points_strategies_long_operation_poin_38e8",
        "long_operation_points_strategies",
        "long_operation_point",
        ["long_operation_point_id"],
        ["id"],
    )
