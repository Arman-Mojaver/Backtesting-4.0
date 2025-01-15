"""
Create resampled point d1 table.

Revision ID: c5382d6238d1
Revises: 15a27170feec
Create Date: 2024-12-06 20:43:06.011049

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

if TYPE_CHECKING:
    from collections.abc import Sequence

revision: str = "c5382d6238d1"
down_revision: str | None = "15a27170feec"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    high_low_order_type = postgresql.ENUM(
        "high_first",
        "low_first",
        "undefined",
        name="highloworder",
        create_type=False,
    )
    high_low_order_type.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "resampled_point_d1",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("datetime", sa.Date(), nullable=False),
        sa.Column("instrument", sa.String(), nullable=False),
        sa.Column("open", sa.Float(), nullable=False),
        sa.Column("high", sa.Float(), nullable=False),
        sa.Column("low", sa.Float(), nullable=False),
        sa.Column("close", sa.Float(), nullable=False),
        sa.Column("volume", sa.Integer(), nullable=False),
        sa.Column("high_low_order", high_low_order_type, nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_resampled_point_d1")),
        sa.UniqueConstraint(
            "datetime",
            "instrument",
            name="uq_datetime_instrument_resampled_d1",
        ),
    )


def downgrade() -> None:
    op.drop_table("resampled_point_d1")
    high_low_order_type = postgresql.ENUM(
        "high_first",
        "low_first",
        "undefined",
        name="highloworder",
        create_type=False,
    )
    high_low_order_type.drop(op.get_bind())
