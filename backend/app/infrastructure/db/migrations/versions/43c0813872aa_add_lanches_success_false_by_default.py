"""add lanches success false by default

Revision ID: 43c0813872aa
Revises: 75b48a2427a3
Create Date: 2025-02-06 09:38:10.798425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '43c0813872aa'
down_revision: Union[str, None] = '75b48a2427a3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
