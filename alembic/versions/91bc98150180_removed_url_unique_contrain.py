"""removed url unique contrain

Revision ID: 91bc98150180
Revises: d6f52d5dcd40
Create Date: 2024-04-15 17:54:41.642942

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91bc98150180'
down_revision: Union[str, None] = 'd6f52d5dcd40'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('short_urls_url_key', 'short_urls', type_='unique')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('short_urls_url_key', 'short_urls', ['url'])
    # ### end Alembic commands ###