"""Removed emplid-based FK from mds_person_middle_name.

Revision ID: 428acfd4f0c9
Revises: bf1225fa63af
Create Date: 2017-04-15 13:06:45.417131

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '428acfd4f0c9'
down_revision = 'bf1225fa63af'
branch_labels = None
depends_on = None

def upgrade():
  # Alter PKs:
  op.drop_constraint(
    'SYS_C00264312',
    'mds_person_middle_name',
    type_='primary'
  )
  op.create_primary_key(
    None,
    'mds_person_middle_name',
    ['uuid', 'timestamp']
  )

  # Make emplid nullable (this should remove an index that would otherwise cause problems):
  op.alter_column(
    'mds_person_middle_name',
    'emplid',
    existing_type=sa.VARCHAR(length=11),
    nullable=True
  )

  # Remove emplid FK:
  op.drop_constraint('SYS_C00281673', 'mds_person_middle_name', type_='foreignkey')

  # Remove emplid column:
  op.drop_column('mds_person_middle_name', 'emplid')

def downgrade():
  # Re-create emplid column:
  op.add_column('mds_person_middle_name', sa.Column('emplid', sa.VARCHAR(length=11), nullable=True))

  # Probably need an emplid re-populating step here...

  # Re-create old emplid FK:
  op.create_foreign_key('SYS_C00281673', 'mds_person_middle_name', 'mds_person_emplid', ['emplid'], ['emplid'], ondelete='CASCADE')

  # Drop new PK and restore old emplid-based PK:
  op.drop_constraint(
    None, # Not sure this will work. Would probably have to add the Oracle-generated name.
    'mds_person_middle_name',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00264312',
    'mds_person_middle_name',
    ['emplid','timestamp']
  )

