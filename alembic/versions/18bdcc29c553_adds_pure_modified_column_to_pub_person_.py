"""Adds pure_modified column to pub, person, and pure_org.

Revision ID: 18bdcc29c553
Revises: 849c87f1c8e4
Create Date: 2018-05-30 20:14:39.507544

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '18bdcc29c553'
down_revision = '849c87f1c8e4'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('person', sa.Column('pure_modified', sa.DateTime(), nullable=True))
    op.add_column('pub', sa.Column('pure_modified', sa.DateTime(), nullable=True))
    op.add_column('pure_org', sa.Column('pure_modified', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('pure_org', 'pure_modified')
    op.drop_column('pub', 'pure_modified')
    op.drop_column('person', 'pure_modified')
