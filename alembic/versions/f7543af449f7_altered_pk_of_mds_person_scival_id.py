"""Altered PK of mds_person_scival_id.

Revision ID: f7543af449f7
Revises: 50860575f1fa
Create Date: 2017-04-15 13:54:49.744343

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'f7543af449f7'
down_revision = '50860575f1fa'
branch_labels = None
depends_on = None

def upgrade():
  op.alter_column(
    'mds_person_scival_id',
    'scival_id',
    existing_type=oracle.NUMBER(scale=0, asdecimal=False),
    nullable=True
  )
  op.drop_constraint(
    'SYS_C00264330',
    'mds_person_scival_id',
    type_='primary'
  )
  op.create_primary_key(
    None,
    'mds_person_scival_id',
    ['uuid', 'timestamp']
  )

def downgrade():
  op.alter_column(
    'mds_person_scival_id',
    'scival_id',
    existing_type=oracle.NUMBER(scale=0, asdecimal=False),
    nullable=False
  )

  # Drop new PK and restore old emplid-based PK:
  op.drop_constraint(
    None, # Not sure this will work. Would probably have to add the Oracle-generated name.
    'mds_person_scival_id',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00264330',
    'mds_person_scival_id',
    ['scival_id']
  )
