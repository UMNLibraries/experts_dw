"""Altered PK of mds_person_emplid.

Revision ID: cc093ad8dde6
Revises: f7543af449f7
Create Date: 2017-04-15 14:03:05.447318

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cc093ad8dde6'
down_revision = 'f7543af449f7'
branch_labels = None
depends_on = None

def upgrade():
  op.alter_column(
    'mds_person_emplid',
    'emplid',
    existing_type=sa.VARCHAR(length=11),
    nullable=True
  )
  op.drop_constraint(
    'SYS_C00280234',
    'mds_person_emplid',
    type_='primary'
  )
  op.create_primary_key(
    None,
    'mds_person_emplid',
    ['uuid', 'timestamp']
  )

def downgrade():
  op.alter_column(
    'mds_person_emplid',
    'emplid',
    existing_type=sa.VARCHAR(length=11),
    nullable=False
  )

  # Drop new PK and restore old emplid-based PK:
  op.drop_constraint(
    None, # Not sure this will work. Would probably have to add the Oracle-generated name.
    'mds_person_emplid',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00280234',
    'mds_person_emplid',
    ['emplid']
  )
