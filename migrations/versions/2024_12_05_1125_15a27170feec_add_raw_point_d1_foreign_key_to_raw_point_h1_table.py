"""
Add raw_point_d1 foreign key to raw_point_h1 table.

Revision ID: 15a27170feec
Revises: 5ef9cb0fed6a
Create Date: 2024-12-05 11:25:15.289438

"""

from __future__ import annotations

from typing import TYPE_CHECKING

import sqlalchemy as sa
from alembic import op

if TYPE_CHECKING:
    from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "15a27170feec"
down_revision: str | None = "5ef9cb0fed6a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "raw_point_h1", sa.Column("raw_point_d1_id", sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        op.f("fk_raw_point_h1_raw_point_d1_id_raw_point_d1"),
        "raw_point_h1",
        "raw_point_d1",
        ["raw_point_d1_id"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        op.f("fk_raw_point_h1_raw_point_d1_id_raw_point_d1"),
        "raw_point_h1",
        type_="foreignkey",
    )
    op.drop_column("raw_point_h1", "raw_point_d1_id")
