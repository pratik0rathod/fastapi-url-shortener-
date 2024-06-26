"""fixed username

Revision ID: d40b234eff43
Revises: 473fa845dc1e
Create Date: 2024-04-15 10:24:22.106984

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd40b234eff43'
down_revision: Union[str, None] = '473fa845dc1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('username', sa.String(), nullable=False))
    op.drop_constraint('User_usernmae_key', 'User', type_='unique')
    op.create_unique_constraint(None, 'User', ['username'])
    op.drop_column('User', 'usernmae')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('User', sa.Column('usernmae', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'User', type_='unique')
    op.create_unique_constraint('User_usernmae_key', 'User', ['usernmae'])
    op.drop_column('User', 'username')
    # ### end Alembic commands ###
