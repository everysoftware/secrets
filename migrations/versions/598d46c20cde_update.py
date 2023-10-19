"""update

Revision ID: 598d46c20cde
Revises: 3ace414026c8
Create Date: 2023-10-19 16:29:06.266097

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '598d46c20cde'
down_revision: Union[str, None] = '3ace414026c8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
