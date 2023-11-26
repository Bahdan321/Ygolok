"""add unique to owners inn

Revision ID: ea3ce74a3879
Revises: 1f2e7934b55f
Create Date: 2023-11-19 23:02:44.853959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea3ce74a3879'
down_revision: Union[str, None] = '1f2e7934b55f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'organizations', ['inn'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'organizations', type_='unique')
    # ### end Alembic commands ###