"""
Create long operation point table.

Revision ID: 3899a31bcc84
Revises: 18bbf1e0db64
Create Date: 2024-12-21 11:42:19.420607

"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3899a31bcc84"
down_revision: str | None = "18bbf1e0db64"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "long_operation_point",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("instrument", sa.String(), nullable=False),
        sa.Column("datetime", sa.Date(), nullable=False),
        sa.Column("result", sa.Integer(), nullable=False),
        sa.Column("tp", sa.Integer(), nullable=False),
        sa.Column("sl", sa.Integer(), nullable=False),
        sa.Column("long_balance", sa.ARRAY(sa.Integer()), nullable=False),
        sa.Column("money_management_strategy_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["money_management_strategy_id"],
            ["money_management_strategy.id"],
            name=op.f(
                "fk_long_operation_point_money_management_strategy_id_money_management_strategy"
            ),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_long_operation_point")),
    )


def downgrade() -> None:
    op.drop_table("long_operation_point")
