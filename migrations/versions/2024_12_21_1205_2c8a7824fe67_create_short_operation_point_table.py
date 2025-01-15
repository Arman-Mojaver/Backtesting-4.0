"""
Create short operation point table.

Revision ID: 2c8a7824fe67
Revises: 3899a31bcc84
Create Date: 2024-12-21 12:05:03.919677

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "2c8a7824fe67"
down_revision: str | None = "3899a31bcc84"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "short_operation_point",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("instrument", sa.String(), nullable=False),
        sa.Column("datetime", sa.Date(), nullable=False),
        sa.Column("result", sa.Integer(), nullable=False),
        sa.Column("tp", sa.Integer(), nullable=False),
        sa.Column("sl", sa.Integer(), nullable=False),
        sa.Column("short_balance", sa.ARRAY(sa.Integer()), nullable=False),
        sa.Column("money_management_strategy_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["money_management_strategy_id"],
            ["money_management_strategy.id"],
            name=op.f(
                "fk_short_operation_point_money_management_strategy_id_money_management_strategy"
            ),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_short_operation_point")),
    )


def downgrade() -> None:
    op.drop_table("short_operation_point")
