"""Adds an internet_id column to umn_data_error.

Revision ID: 0abe014bc8b8
Revises: 914642b6f2bd
Create Date: 2019-09-24 13:06:02.414116

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0abe014bc8b8'
down_revision = '914642b6f2bd'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('umn_data_error', sa.Column('internet_id', sa.String(15), nullable=True))

def downgrade():
    op.drop_column('umn_data_error', 'internet_id')
