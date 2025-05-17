"""
Add timestamp to operation_point table.

Revision ID: 07c2a22ba073
Revises: 0e8f72e42262
Create Date: 2025-05-11 15:43:40.227682

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "07c2a22ba073"
down_revision: str | None = "0e8f72e42262"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "long_operation_point", sa.Column("timestamp", sa.Integer(), nullable=False)
    )
    op.add_column(
        "short_operation_point", sa.Column("timestamp", sa.Integer(), nullable=False)
    )


def downgrade() -> None:
    op.drop_column("short_operation_point", "timestamp")
    op.drop_column("long_operation_point", "timestamp")
