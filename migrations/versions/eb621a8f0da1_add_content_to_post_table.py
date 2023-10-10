"""add content to post table

Revision ID: eb621a8f0da1
Revises: f628cf291a93
Create Date: 2023-10-09 16:31:36.293416

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "eb621a8f0da1"
down_revision: Union[str, None] = "f628cf291a93"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
