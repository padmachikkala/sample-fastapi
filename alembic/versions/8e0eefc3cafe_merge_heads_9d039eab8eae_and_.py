"""merge heads 9d039eab8eae and fdf10a59014f

Revision ID: 8e0eefc3cafe
Revises: 9d039eab8eae, fdf10a59014f
Create Date: 2023-12-27 15:10:49.952275

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e0eefc3cafe'
down_revision: Union[str, None] = ('9d039eab8eae', 'fdf10a59014f')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
