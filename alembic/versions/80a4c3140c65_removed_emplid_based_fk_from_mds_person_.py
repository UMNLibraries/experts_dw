"""Removed emplid-based FK from mds_person_tenure_flag.

Revision ID: 80a4c3140c65
Revises: cd7ddc60af98
Create Date: 2017-04-15 13:30:06.369029

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '80a4c3140c65'
down_revision = 'cd7ddc60af98'
branch_labels = None
depends_on = None

def upgrade():
  # Alter PKs:
  op.drop_constraint(
    'SYS_C00264334',
    'mds_person_tenure_flag',
    type_='primary'
  )
  op.create_primary_key(
    None,
    'mds_person_tenure_flag',
    ['uuid', 'timestamp']
  )

  # Make emplid nullable (this should remove an index that would otherwise cause problems):
  op.alter_column(
    'mds_person_tenure_flag',
    'emplid',
    existing_type=sa.VARCHAR(length=11),
    nullable=True
  )

  # Remove emplid FK:
  op.drop_constraint('SYS_C00281678', 'mds_person_tenure_flag', type_='foreignkey')

  # Remove emplid column:
  op.drop_column('mds_person_tenure_flag', 'emplid')

def downgrade():
  # Re-create emplid column:
  op.add_column('mds_person_tenure_flag', sa.Column('emplid', sa.VARCHAR(length=11), nullable=True))

  # Probably need an emplid re-populating step here...

  # Re-create old emplid FK:
  op.create_foreign_key('SYS_C00281678', 'mds_person_tenure_flag', 'mds_person_emplid', ['emplid'], ['emplid'], ondelete='CASCADE')

  # Drop new PK and restore old emplid-based PK:
  op.drop_constraint(
    None, # Not sure this will work. Would probably have to add the Oracle-generated name.
    'mds_person_tenure_flag',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00264334',
    'mds_person_tenure_flag',
    ['emplid','timestamp']
  )

