"""
Remove min_annual_roi column from strategy table.

Revision ID: 4b559a42f5ca
Revises: db78ce260a82
Create Date: 2025-03-18 08:09:02.421227

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "4b559a42f5ca"
down_revision: str | None = "db78ce260a82"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_column("strategy", "min_annual_roi")


def downgrade() -> None:
    op.add_column("strategy", sa.Column("min_annual_roi", sa.Float(), nullable=False))
