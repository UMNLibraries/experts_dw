"""Removed emplid from mds_person_internet_id.

Revision ID: b27adb379817
Revises: d62895e358d3
Create Date: 2017-04-15 11:47:39.622471

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b27adb379817'
down_revision = 'd62895e358d3'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_column('mds_person_internet_id', 'emplid')

def downgrade():
  op.add_column('mds_person_internet_id', sa.Column('emplid', sa.VARCHAR(length=11), nullable=True))
