"""
Add short_operation_point_strategy many-to-many relationship.

Revision ID: 0e8f72e42262
Revises: 1c45e6c21222
Create Date: 2025-04-24 17:54:36.758938

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "0e8f72e42262"
down_revision: str | None = "1c45e6c21222"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_foreign_key(
        op.f("fk_short_operation_points_strategies_strategy_id_strategy"),
        "short_operation_points_strategies",
        "strategy",
        ["strategy_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        op.f(
            "fk_short_operation_points_strategies_short_operation_point_id_short_operation_point"
        ),
        "short_operation_points_strategies",
        "short_operation_point",
        ["short_operation_point_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f(
            "fk_short_operation_points_strategies_short_operation_point_id_short_operation_point"
        ),
        "short_operation_points_strategies",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("fk_short_operation_points_strategies_strategy_id_strategy"),
        "short_operation_points_strategies",
        type_="foreignkey",
    )
