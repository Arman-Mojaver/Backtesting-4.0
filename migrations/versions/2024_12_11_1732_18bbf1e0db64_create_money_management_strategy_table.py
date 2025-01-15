"""
Create money management strategy table.

Revision ID: 18bbf1e0db64
Revises: c5382d6238d1
Create Date: 2024-12-11 17:32:02.820291

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

if TYPE_CHECKING:
    from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "18bbf1e0db64"
down_revision: str | None = "c5382d6238d1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    money_management_strategy_type = postgresql.ENUM(
        "atr",
        name="moneymanagementstrategytype",
        create_type=False,
    )
    money_management_strategy_type.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "money_management_strategy",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("type", money_management_strategy_type, nullable=False),
        sa.Column("tp_multiplier", sa.Float(), nullable=False),
        sa.Column("sl_multiplier", sa.Float(), nullable=False),
        sa.Column("parameters", sa.JSON(), nullable=False),
        sa.Column("identifier", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_money_management_strategy")),
        sa.UniqueConstraint("identifier", name="uq_money_management_strategy_identifier"),
    )


def downgrade() -> None:
    op.drop_table("money_management_strategy")

    money_management_strategy_type = postgresql.ENUM(
        "atr",
        name="moneymanagementstrategytype",
        create_type=False,
    )
    money_management_strategy_type.drop(op.get_bind())
