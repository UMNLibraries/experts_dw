"""Dropping pure_internal_org.pure_uuid for now.

Revision ID: d79bd28cc144
Revises: 64ffc2f4572f
Create Date: 2017-05-02 15:40:09.371628

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'd79bd28cc144'
down_revision = '64ffc2f4572f'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_column('pure_internal_org', 'pure_uuid')

def downgrade():
  op.add_column('pure_internal_org', sa.Column('pure_uuid', sa.VARCHAR(length=36), nullable=False))
