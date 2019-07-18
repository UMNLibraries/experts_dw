"""Adds umn_data_error.jobcode_descr.

Revision ID: be5f8a94028b
Revises: 58f9c020e85b
Create Date: 2019-07-18 13:24:58.442648

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'be5f8a94028b'
down_revision = '58f9c020e85b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('umn_data_error', sa.Column('jobcode_descr', sa.String(length=35), nullable=True))

def downgrade():
    op.drop_column('umn_data_error', 'jobcode_descr')
