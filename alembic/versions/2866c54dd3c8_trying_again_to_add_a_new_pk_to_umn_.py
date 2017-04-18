"""Trying again to add a new PK to umn_dept_pure_org_map.

Revision ID: 2866c54dd3c8
Revises: 25be388a4614
Create Date: 2017-04-18 10:12:51.009934

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2866c54dd3c8'
down_revision = '25be388a4614'
branch_labels = None
depends_on = None

def upgrade():
  sa.PrimaryKeyConstraint('umn_dept_id')

def downgrade():
  # Probably would need to replace None with the Oracle-generated name here:
  op.drop_constraint(None, 'umn_dept_pure_org_map', type_='primary')
