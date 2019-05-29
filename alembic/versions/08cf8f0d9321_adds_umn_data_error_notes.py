"""Adds umn_data_error.notes.

Revision ID: 08cf8f0d9321
Revises: 960fc1e68982
Create Date: 2019-05-24 15:35:43.003176

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '08cf8f0d9321'
down_revision = '960fc1e68982'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('umn_data_error', sa.Column('notes', sa.Text(), nullable=True))

def downgrade():
    op.drop_column('umn_data_error', 'notes')
