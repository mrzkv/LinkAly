"""fix indexes

Revision ID: f1fa4925dd69
Revises: 
Create Date: 2025-05-23 10:48:27.010559

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'f1fa4925dd69'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('url_pairs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('short_url', sa.VARCHAR(length=30), nullable=False),
    sa.Column('real_url', sa.VARCHAR(length=512), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_url_pairs'))
    )
    op.create_index('ix_url_pairs_real_url', 'url_pairs', ['real_url'], unique=False, postgresql_using='hash')
    op.create_index('ix_url_pairs_short_url', 'url_pairs', ['short_url'], unique=False, postgresql_using='hash')


def downgrade() -> None:
    op.drop_index('ix_url_pairs_short_url', table_name='url_pairs', postgresql_using='hash')
    op.drop_index('ix_url_pairs_real_url', table_name='url_pairs', postgresql_using='hash')
    op.drop_table('url_pairs')