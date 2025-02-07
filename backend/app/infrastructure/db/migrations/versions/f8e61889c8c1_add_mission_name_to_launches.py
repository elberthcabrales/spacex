"""add mission name to launches

Revision ID: f8e61889c8c1
Revises: 066d4668fd65
Create Date: 2025-02-05 01:29:19.352783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision: str = 'f8e61889c8c1'
down_revision: Union[str, None] = '066d4668fd65'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('launches', sa.Column('mission_name', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('launches', 'mission_name')
    # ### end Alembic commands ###
