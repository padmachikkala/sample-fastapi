"""add user table

Revision ID: 6f55f26beb28
Revises: 6a6e3e7bcdd0
Create Date: 2023-12-26 16:24:48.270434

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f55f26beb28'
down_revision: Union[str, None] = '6a6e3e7bcdd0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')                
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
