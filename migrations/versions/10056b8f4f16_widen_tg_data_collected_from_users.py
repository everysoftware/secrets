"""widen tg data collected from users

Revision ID: 10056b8f4f16
Revises: ddbbd9d51ac4
Create Date: 2023-10-23 00:35:37.090871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10056b8f4f16'
down_revision: Union[str, None] = 'ddbbd9d51ac4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('comments')
    op.drop_table('records')
    op.drop_table('auth_data')
    op.drop_table('users')
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=True),
    sa.Column('language_code', sa.String(), nullable=True),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('reg_date', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('id'),
    sa.UniqueConstraint('user_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('auth_data',
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('account_password', sa.VARCHAR(length=64), nullable=False),
    sa.Column('master_password', sa.VARCHAR(length=64), nullable=False),
    sa.Column('salt', sa.LargeBinary(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_table('records',
    sa.Column('id', sa.BigInteger(), sa.Identity(always=False), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('url', sa.VARCHAR(length=64), nullable=False),
    sa.Column('title', sa.VARCHAR(length=64), nullable=False),
    sa.Column('username', sa.LargeBinary(), nullable=True),
    sa.Column('password_', sa.LargeBinary(), nullable=True),
    sa.Column('salt', sa.LargeBinary(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('record_id', sa.BigInteger(), nullable=False),
    sa.Column('text', sa.VARCHAR(length=512), nullable=True),
    sa.ForeignKeyConstraint(['record_id'], ['records.id'], ),
    sa.PrimaryKeyConstraint('record_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
