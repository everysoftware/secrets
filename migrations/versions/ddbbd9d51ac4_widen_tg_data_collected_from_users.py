
"""widen tg data collected from users

Revision ID: ddbbd9d51ac4
Revises: 89dd36104c77
Create Date: 2023-10-23 00:34:20.784655

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ddbbd9d51ac4'
down_revision: Union[str, None] = '89dd36104c77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
