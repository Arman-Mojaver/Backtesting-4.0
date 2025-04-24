"""
Add long_operation_point_strategy many-to-many relationship.

Revision ID: 1c45e6c21222
Revises: 72cf3e744950
Create Date: 2025-04-24 16:38:26.268393

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "1c45e6c21222"
down_revision: str | None = "72cf3e744950"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_foreign_key(
        op.f("fk_long_operation_points_strategies_strategy_id_strategy"),
        "long_operation_points_strategies",
        "strategy",
        ["strategy_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f(
            "fk_long_operation_points_strategies_long_operation_point_id_long_operation_point"
        ),
        "long_operation_points_strategies",
        "long_operation_point",
        ["long_operation_point_id"],
        ["id"],
        ondelete="CASCADE",
    )
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
    op.create_foreign_key(
        op.f(
            "fk_long_operation_points_strategies_long_operation_point_id_long_operation_point"
        ),
        "long_operation_points_strategies",
        "long_operation_point",
        ["long_operation_point_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f("fk_long_operation_points_strategies_strategy_id_strategy"),
        "long_operation_points_strategies",
        "strategy",
        ["strategy_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f(
            "fk_long_operation_points_strategies_long_operation_point_id_long_operation_point"
        ),
        "long_operation_points_strategies",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_long_operation_points_strategies_strategy_id_strategy"),
        "long_operation_points_strategies",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_long_operation_points_strategies_strategy_id_strategy"),
        "long_operation_points_strategies",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f(
            "fk_long_operation_points_strategies_long_operation_point_id_long_operation_point"
        ),
        "long_operation_points_strategies",
        type_="foreignkey",
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
