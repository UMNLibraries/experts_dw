"""Renames umn_data_error.notified to reported.

Revision ID: 24082a82c949
Revises: be5f8a94028b
Create Date: 2019-08-02 11:59:18.473147

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '24082a82c949'
down_revision = 'be5f8a94028b'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('umn_data_error', 'notified', new_column_name='reported')

def downgrade():
    op.alter_column('umn_data_error', 'reported', new_column_name='notified')
