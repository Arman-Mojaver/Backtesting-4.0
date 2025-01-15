"""
Create indicator table.

Revision ID: c85eba75ccd9
Revises: 2c8a7824fe67
Create Date: 2024-12-31 10:13:45.058860

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "c85eba75ccd9"
down_revision: str | None = "2c8a7824fe67"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "indicator",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("parameters", sa.JSON(), nullable=False),
        sa.Column("identifier", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_indicator")),
        sa.UniqueConstraint("identifier", name="uq_indicator_identifier"),
    )


def downgrade() -> None:
    op.drop_table("indicator")
