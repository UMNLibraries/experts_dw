"""Removed the pure_org.pure_id FK from umn_person_pure_org_map.

Revision ID: dfc4d651ed31
Revises: 2254ed89c1d8
Create Date: 2017-05-03 15:12:09.088180

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'dfc4d651ed31'
down_revision = '2254ed89c1d8'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_constraint('SYS_C00284284', 'umn_person_pure_org_map', type_='foreignkey')

def downgrade():
  op.create_foreign_key('SYS_C00284284', 'umn_person_pure_org_map', 'pure_org', ['pure_org_id'], ['pure_id'])
