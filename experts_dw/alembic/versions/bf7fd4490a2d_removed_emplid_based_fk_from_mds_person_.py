"""Removed emplid-based FK from mds_person_name_suffix.

Revision ID: bf7fd4490a2d
Revises: 428acfd4f0c9
Create Date: 2017-04-15 13:13:20.527710

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bf7fd4490a2d'
down_revision = '428acfd4f0c9'
branch_labels = None
depends_on = None

def upgrade():
  # Alter PKs:
  op.drop_constraint(
    'SYS_C00264316',
    'mds_person_name_suffix',
    type_='primary'
  )
  op.create_primary_key(
    None,
    'mds_person_name_suffix',
    ['uuid', 'timestamp']
  )

  # Make emplid nullable (this should remove an index that would otherwise cause problems):
  op.alter_column(
    'mds_person_name_suffix',
    'emplid',
    existing_type=sa.VARCHAR(length=11),
    nullable=True
  )

  # Remove emplid FK:
  op.drop_constraint('SYS_C00281674', 'mds_person_name_suffix', type_='foreignkey')

  # Remove emplid column:
  op.drop_column('mds_person_name_suffix', 'emplid')

def downgrade():
  # Re-create emplid column:
  op.add_column('mds_person_name_suffix', sa.Column('emplid', sa.VARCHAR(length=11), nullable=True))

  # Probably need an emplid re-populating step here...

  # Re-create old emplid FK:
  op.create_foreign_key('SYS_C00281674', 'mds_person_name_suffix', 'mds_person_emplid', ['emplid'], ['emplid'], ondelete='CASCADE')

  # Drop new PK and restore old emplid-based PK:
  op.drop_constraint(
    None, # Not sure this will work. Would probably have to add the Oracle-generated name.
    'mds_person_name_suffix',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00264316',
    'mds_person_name_suffix',
    ['emplid','timestamp']
  )

