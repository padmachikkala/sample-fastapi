""" add content column to posts table

Revision ID: 6a6e3e7bcdd0
Revises: 0ad090d80d72
Create Date: 2023-12-26 16:10:50.728493

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6a6e3e7bcdd0'
down_revision: Union[str, None] = '0ad090d80d72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
