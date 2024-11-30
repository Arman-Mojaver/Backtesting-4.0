"""
Create raw_point_h1 table.

Revision ID: 5ef9cb0fed6a
Revises: 28703852942a
Create Date: 2024-11-30 22:10:36.930306

"""
from __future__ import annotations

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5ef9cb0fed6a"
down_revision: str | None = "28703852942a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "raw_point_h1",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("datetime", sa.DateTime(), nullable=False),
        sa.Column("instrument", sa.String(), nullable=False),
        sa.Column("open", sa.Float(), nullable=False),
        sa.Column("high", sa.Float(), nullable=False),
        sa.Column("low", sa.Float(), nullable=False),
        sa.Column("close", sa.Float(), nullable=False),
        sa.Column("volume", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_raw_point_h1")),
        sa.UniqueConstraint("datetime", "instrument", name="uq_datetime_instrument_h1"),
    )


def downgrade() -> None:
    op.drop_table("raw_point_h1")
