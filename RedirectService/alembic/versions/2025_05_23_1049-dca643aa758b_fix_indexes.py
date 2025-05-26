"""fix indexes

Revision ID: dca643aa758b
Revises: f1fa4925dd69
Create Date: 2025-05-23 10:49:56.510881

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dca643aa758b'
down_revision: Union[str, None] = 'f1fa4925dd69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index('ix_url_pairs_real_url', table_name='url_pairs', postgresql_using='hash')

def downgrade() -> None:
    op.create_index('ix_url_pairs_real_url', 'url_pairs', ['real_url'], unique=False, postgresql_using='hash')