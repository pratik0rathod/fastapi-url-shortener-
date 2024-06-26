"""added user type

Revision ID: be4c773c3105
Revises: 91bc98150180
Create Date: 2024-04-16 12:24:50.634393

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be4c773c3105'
down_revision: Union[str, None] = '91bc98150180'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE TYPE userenum AS ENUM ('SUPER_USER', 'NORMAL_USER', 'ADMIN')")
    op.add_column('User', sa.Column('user_type', sa.Enum('SUPER_USER', 'NORMAL_USER', 'ADMIN', name='userenum'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('User', 'user_type')
    op.execute("DROP TYPE userenum")
    # ### end Alembic commands ###
