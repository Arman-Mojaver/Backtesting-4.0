"""
Create raw_point_d1 table.

Revision ID: 28703852942a
Revises:
Create Date: 2024-11-24 11:12:14.262151

"""

from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "28703852942a"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "raw_point_d1",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("datetime", sa.Date(), nullable=False),
        sa.Column("instrument", sa.String(), nullable=False),
        sa.Column("open", sa.Float(), nullable=False),
        sa.Column("high", sa.Float(), nullable=False),
        sa.Column("low", sa.Float(), nullable=False),
        sa.Column("close", sa.Float(), nullable=False),
        sa.Column("volume", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_raw_point_d1")),
        sa.UniqueConstraint("datetime", "instrument", name="uq_datetime_instrument_d1"),
    )


def downgrade() -> None:
    op.drop_table("raw_point_d1")
