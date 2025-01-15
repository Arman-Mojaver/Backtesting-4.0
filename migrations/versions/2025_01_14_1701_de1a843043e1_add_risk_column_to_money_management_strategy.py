"""
Add risk column to money_management_strategy.

Revision ID: de1a843043e1
Revises: c85eba75ccd9
Create Date: 2025-01-14 17:01:26.465748

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "de1a843043e1"
down_revision: str | None = "c85eba75ccd9"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "money_management_strategy", sa.Column("risk", sa.Float(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column("money_management_strategy", "risk")
