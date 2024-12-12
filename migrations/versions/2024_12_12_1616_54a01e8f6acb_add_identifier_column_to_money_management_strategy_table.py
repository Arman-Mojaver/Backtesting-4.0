"""
Add_identifier_column_to_money_management_strategy_table.

Revision ID: 54a01e8f6acb
Revises: 18bbf1e0db64
Create Date: 2024-12-12 16:16:00.473863

"""
from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "54a01e8f6acb"
down_revision: str | None = "18bbf1e0db64"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "money_management_strategy", sa.Column("identifier", sa.String(), nullable=False)
    )
    op.create_unique_constraint(
        "uq_money_management_strategy_identifier",
        "money_management_strategy",
        ["identifier"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_money_management_strategy_identifier",
        "money_management_strategy",
        type_="unique",
    )
    op.drop_column("money_management_strategy", "identifier")
