"""
Add timestamp to resampled_point_d1 table.

Revision ID: d1d7f704903c
Revises: 52988e0269c0
Create Date: 2025-05-17 16:13:15.732588

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "d1d7f704903c"
down_revision: str | None = "52988e0269c0"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "resampled_point_d1", sa.Column("timestamp", sa.Integer(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column("resampled_point_d1", "timestamp")
