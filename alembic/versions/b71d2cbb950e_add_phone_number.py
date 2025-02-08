"""add phone number

Revision ID: b71d2cbb950e
Revises: 7c58111cd8f5
Create Date: 2025-02-08 13:50:36.392864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b71d2cbb950e'
down_revision: Union[str, None] = '7c58111cd8f5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users' , 
                  sa.Column('number' , sa.Integer, nullable=False,server_default='1010101010'))


def downgrade() -> None:
    op.drop_column('users','number')
    pass
