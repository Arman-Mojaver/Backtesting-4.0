"""
Add raw_point_d1_instrument_datetime_unique_constraint.

Revision ID: 809f59e05feb
Revises: 28703852942a
Create Date: 2024-11-24 12:08:13.275822

"""
from __future__ import annotations

from typing import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "809f59e05feb"
down_revision: str | None = "28703852942a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_datetime_instrument",
        "raw_point_d1",
        ["datetime", "instrument"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_datetime_instrument",
        "raw_point_d1",
        type_="unique",
    )
