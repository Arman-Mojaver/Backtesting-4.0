"""
Add instrument column to strategy table.

Revision ID: 5fbc5e9726cd
Revises: d1d7f704903c
Create Date: 2025-06-12 15:45:24.607395

"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5fbc5e9726cd"
down_revision: str | None = "d1d7f704903c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("strategy", sa.Column("instrument", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("strategy", "instrument")
