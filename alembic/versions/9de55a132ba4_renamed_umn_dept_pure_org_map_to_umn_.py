"""Renamed umn_dept_pure_org_map to umn_dept_pure_org.

Revision ID: 9de55a132ba4
Revises: ecc2159ed138
Create Date: 2017-05-04 19:09:36.695498

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '9de55a132ba4'
down_revision = 'ecc2159ed138'
branch_labels = None
depends_on = None

def upgrade():
  op.rename_table('umn_dept_pure_org_map', 'umn_dept_pure_org')

def downgrade():
  op.rename_table('umn_dept_pure_org', 'umn_dept_pure_org_map')
