"""Removed emplid-based FK from mds_person_last_name.

Revision ID: adf4a4c012c9
Revises: b27adb379817
Create Date: 2017-04-15 12:06:46.413719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adf4a4c012c9'
down_revision = 'b27adb379817'
branch_labels = None
depends_on = None

def upgrade():
  # Alter PKs:
  op.drop_constraint(
    'SYS_C00264308',
    'mds_person_last_name',
    type_='primary'
  )
  op.create_primary_key(
    None,
    'mds_person_last_name',
    ['uuid', 'timestamp']
  )

  # Make emplid nullable (this should remove an index that would otherwise cause problems):
  op.alter_column(
    'mds_person_last_name',
    'emplid',
    existing_type=sa.VARCHAR(length=11),
    nullable=True
  )

  # Remove emplid FK:
  op.drop_constraint('SYS_C00281672', 'mds_person_last_name', type_='foreignkey')

  # Remove emplid column:
  op.drop_column('mds_person_last_name', 'emplid')

def downgrade():
  # Re-create emplid column:
  op.add_column('mds_person_last_name', sa.Column('emplid', sa.VARCHAR(length=11), nullable=True))

  # Probably need an emplid re-populating step here...

  # Re-create old emplid FK:
  op.create_foreign_key('SYS_C00281672', 'mds_person_last_name', 'mds_person_emplid', ['emplid'], ['emplid'], ondelete='CASCADE')

  # Drop new PK and restore old emplid-based PK:
  op.drop_constraint(
    None, # Not sure this will work. Would probably have to add the Oracle-generated name.
    'mds_person_last_name',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00264308',
    'mds_person_last_name',
    ['emplid','timestamp']
  )

