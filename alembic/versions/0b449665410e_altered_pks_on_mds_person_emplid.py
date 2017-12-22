"""Altered PKs on mds_person_emplid.

Revision ID: 0b449665410e
Revises: 7e30120a64b7
Create Date: 2017-04-15 11:05:39.797757

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0b449665410e'
down_revision = '7e30120a64b7'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_constraint(
    'SYS_C00264304',
    'mds_person_internet_id',
    type_='primary'
  )
  op.alter_column(
    'mds_person_internet_id',
    'emplid',
    existing_type=sa.VARCHAR(length=11),
    nullable=True
  )
  op.create_primary_key(
    None,
    'mds_person_internet_id',
    ['uuid', 'timestamp']
  )

def downgrade():
  op.drop_constraint(
    None, # Not sure this will work. Would probably have to add the Oracle-generated name.
    'mds_person_internet_id',
    type_='primary'
  )
  op.create_primary_key(
    None,
    'mds_person_internet_id',
    ['emplid','timestamp']
  )
