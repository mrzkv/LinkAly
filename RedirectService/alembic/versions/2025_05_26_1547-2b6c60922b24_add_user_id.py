"""add user_id

Revision ID: 2b6c60922b24
Revises: dca643aa758b
Create Date: 2025-05-26 15:47:06.434118

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b6c60922b24'
down_revision: Union[str, None] = 'dca643aa758b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('url_pairs', sa.Column('creator_id', sa.INTEGER(), nullable=False))


def downgrade() -> None:
    op.drop_column('url_pairs', 'creator_id')