"""Altered PK of mds_person_first_name.

Revision ID: bf1225fa63af
Revises: 10359d213c15
Create Date: 2017-04-15 13:00:57.064928

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf1225fa63af'
down_revision = '10359d213c15'
branch_labels = None
depends_on = None

def upgrade():
  op.create_primary_key(
    None,
    'mds_person_first_name',
    ['uuid', 'timestamp']
  )

def downgrade():
  op.drop_constraint(
    None, # Not sure this will work. Would probably have to add the Oracle-generated name.
    'mds_person_first_name',
    type_='primary'
  )
