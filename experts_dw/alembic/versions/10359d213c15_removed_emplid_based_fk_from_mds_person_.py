"""Removed emplid-based FK from mds_person_preferred_name.

Revision ID: 10359d213c15
Revises: adf4a4c012c9
Create Date: 2017-04-15 12:21:14.307338

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '10359d213c15'
down_revision = 'adf4a4c012c9'
branch_labels = None
depends_on = None

def upgrade():
  # Alter PKs:
  op.drop_constraint(
    'SYS_C00264320',
    'mds_person_preferred_name',
    type_='primary'
  )
  op.create_primary_key(
    None,
    'mds_person_preferred_name',
    ['uuid', 'timestamp']
  )

  # Make emplid nullable (this should remove an index that would otherwise cause problems):
  op.alter_column(
    'mds_person_preferred_name',
    'emplid',
    existing_type=sa.VARCHAR(length=11),
    nullable=True
  )

  # Remove emplid FK:
  op.drop_constraint('SYS_C00281675', 'mds_person_preferred_name', type_='foreignkey')

  # Remove emplid column:
  op.drop_column('mds_person_preferred_name', 'emplid')

def downgrade():
  # Re-create emplid column:
  op.add_column('mds_person_preferred_name', sa.Column('emplid', sa.VARCHAR(length=11), nullable=True))

  # Probably need an emplid re-populating step here...

  # Re-create old emplid FK:
  op.create_foreign_key('SYS_C00281675', 'mds_person_preferred_name', 'mds_person_emplid', ['emplid'], ['emplid'], ondelete='CASCADE')

  # Drop new PK and restore old emplid-based PK:
  op.drop_constraint(
    None, # Not sure this will work. Would probably have to add the Oracle-generated name.
    'mds_person_preferred_name',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00264320',
    'mds_person_preferred_name',
    ['emplid','timestamp']
  )
