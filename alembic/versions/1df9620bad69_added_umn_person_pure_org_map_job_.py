"""Added umn_person_pure_org_map.job_description to the PK.

Revision ID: 1df9620bad69
Revises: e7fcfed629f8
Create Date: 2017-04-21 14:18:00.101721

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1df9620bad69'
down_revision = 'e7fcfed629f8'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_constraint('SYS_C00284282', 'umn_person_pure_org_map', type_='primary')
  # This didn't work--needed to do it manually:
  sa.PrimaryKeyConstraint('person_uuid','pure_org_id','job_description')

def downgrade():
  # Probably would need to add the constraint name before running this:
  op.drop_constraint(None, 'umn_person_pure_org_map', type_='primary')
  sa.PrimaryKeyConstraint('person_uuid','pure_org_id')
