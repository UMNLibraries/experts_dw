"""Removed emplid-based FK from mds_person_primary_empl_rcdno.

Revision ID: 50860575f1fa
Revises: e5ae8e58cf03
Create Date: 2017-04-15 13:47:48.623246

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '50860575f1fa'
down_revision = 'e5ae8e58cf03'
branch_labels = None
depends_on = None

def upgrade():
  # Alter PKs:
  op.drop_constraint(
    'SYS_C00264342',
    'mds_person_primary_empl_rcdno',
    type_='primary'
  )
  op.create_primary_key(
    None,
    'mds_person_primary_empl_rcdno',
    ['uuid', 'timestamp']
  )

  # Make emplid nullable (this should remove an index that would otherwise cause problems):
  op.alter_column(
    'mds_person_primary_empl_rcdno',
    'emplid',
    existing_type=sa.VARCHAR(length=11),
    nullable=True
  )

  # Remove emplid FK:
  op.drop_constraint('SYS_C00281676', 'mds_person_primary_empl_rcdno', type_='foreignkey')

  # Remove emplid column:
  op.drop_column('mds_person_primary_empl_rcdno', 'emplid')

def downgrade():
  # Re-create emplid column:
  op.add_column('mds_person_primary_empl_rcdno', sa.Column('emplid', sa.VARCHAR(length=11), nullable=True))

  # Probably need an emplid re-populating step here...

  # Re-create old emplid FK:
  op.create_foreign_key('SYS_C00281676', 'mds_person_primary_empl_rcdno', 'mds_person_emplid', ['emplid'], ['emplid'], ondelete='CASCADE')

  # Drop new PK and restore old emplid-based PK:
  op.drop_constraint(
    None, # Not sure this will work. Would probably have to add the Oracle-generated name.
    'mds_person_primary_empl_rcdno',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00264342',
    'mds_person_primary_empl_rcdno',
    ['emplid','timestamp']
  )

