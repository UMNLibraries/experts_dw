"""Removed emplid-based PK from mds_person_instl_email_addr.

Revision ID: cd7ddc60af98
Revises: bf7fd4490a2d
Create Date: 2017-04-15 13:22:08.380402

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'cd7ddc60af98'
down_revision = 'bf7fd4490a2d'
branch_labels = None
depends_on = None

def upgrade():
  # Alter PKs:
  op.drop_constraint(
    'SYS_C00264300',
    'mds_person_instl_email_addr',
    type_='primary'
  )
  op.create_primary_key(
    None,
    'mds_person_instl_email_addr',
    ['uuid', 'timestamp']
  )

  # Make emplid nullable (this should remove an index that would otherwise cause problems):
  op.alter_column(
    'mds_person_instl_email_addr',
    'emplid',
    existing_type=sa.VARCHAR(length=11),
    nullable=True
  )

  # Remove emplid column:
  op.drop_column('mds_person_instl_email_addr', 'emplid')

def downgrade():
  # Re-create emplid column:
  op.add_column('mds_person_instl_email_addr', sa.Column('emplid', sa.VARCHAR(length=11), nullable=True))

  # Probably need an emplid re-populating step here...

  # Drop new PK and restore old emplid-based PK:
  op.drop_constraint(
    None, # Not sure this will work. Would probably have to add the Oracle-generated name.
    'mds_person_instl_email_addr',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00264300',
    'mds_person_instl_email_addr',
    ['emplid','timestamp']
  )

