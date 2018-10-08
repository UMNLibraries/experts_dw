"""Adds pub.pure_(sub)type columns.

Revision ID: 3197ec6cb8c5
Revises: 6b70db12a920
Create Date: 2018-10-08 15:40:46.223025

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '3197ec6cb8c5'
down_revision = '6b70db12a920'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('pub', sa.Column('pure_subtype', sa.String(length=50), nullable=True))
    op.add_column('pub', sa.Column('pure_type', sa.String(length=50), nullable=True))

def downgrade():
    op.drop_column('pub', 'pure_type')
    op.drop_column('pub', 'pure_subtype')
