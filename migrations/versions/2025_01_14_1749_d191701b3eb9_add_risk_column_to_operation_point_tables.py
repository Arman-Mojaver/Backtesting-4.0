"""
Add risk column to long_operation_point and short_operation_point tables.

Revision ID: d191701b3eb9
Revises: de1a843043e1
Create Date: 2025-01-14 17:49:10.970843

"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d191701b3eb9"
down_revision: str | None = "de1a843043e1"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("long_operation_point", sa.Column("risk", sa.Float(), nullable=False))
    op.add_column("short_operation_point", sa.Column("risk", sa.Float(), nullable=False))


def downgrade() -> None:
    op.drop_column("short_operation_point", "risk")
    op.drop_column("long_operation_point", "risk")
