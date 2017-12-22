"""Added cascade on delete to remaining FKs.

Revision ID: 56540801908b
Revises: 233412cbfe1a
Create Date: 2017-04-16 09:58:42.176758

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '56540801908b'
down_revision = '233412cbfe1a'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_constraint('SYS_C00281490', 'mds_person_first_name', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_first_name',
    'mds_person',
    ['uuid'],
    ['uuid'],
    ondelete='CASCADE'
  )

  op.drop_constraint('SYS_C00281486', 'mds_person_instl_email_addr', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_instl_email_addr',
    'mds_person',
    ['uuid'],
    ['uuid'],
    ondelete='CASCADE'
  )

  op.drop_constraint('SYS_C00281488', 'mds_person_internet_id', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_internet_id',
    'mds_person',
    ['uuid'],
    ['uuid'],
    ondelete='CASCADE'
  )

  op.drop_constraint('SYS_C00281492', 'mds_person_last_name', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_last_name',
    'mds_person',
    ['uuid'],
    ['uuid'],
    ondelete='CASCADE'
  )

  op.drop_constraint('SYS_C00281494', 'mds_person_middle_name', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_middle_name',
    'mds_person',
    ['uuid'],
    ['uuid'],
    ondelete='CASCADE'
  )

  op.drop_constraint('SYS_C00281496', 'mds_person_name_suffix', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_name_suffix',
    'mds_person',
    ['uuid'],
    ['uuid'],
    ondelete='CASCADE'
  )

  op.drop_constraint('SYS_C00281498', 'mds_person_preferred_name', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_preferred_name',
    'mds_person',
    ['uuid'],
    ['uuid'],
    ondelete='CASCADE'
  )

  op.drop_constraint('SYS_C00281500', 'mds_person_primary_empl_rcdno', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_primary_empl_rcdno',
    'mds_person',
    ['uuid'],
    ['uuid'],
    ondelete='CASCADE'
  )

  op.drop_constraint('SYS_C00281400', 'mds_person_scival_id', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_scival_id',
    'mds_person',
    ['uuid'],
    ['uuid'],
    ondelete='CASCADE'
  )

  op.drop_constraint('SYS_C00281502', 'mds_person_tenure_flag', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_tenure_flag',
    'mds_person',
    ['uuid'],
    ['uuid'],
    ondelete='CASCADE'
  )

  op.drop_constraint('SYS_C00281504', 'mds_person_tenure_track_flag', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_tenure_track_flag',
    'mds_person',
    ['uuid'],
    ['uuid'],
    ondelete='CASCADE'
  )

def downgrade():
  op.drop_constraint(None, 'mds_person_first_name', type_='foreignkey')
  op.create_foreign_key('SYS_C00281490', 'mds_person_first_name', 'mds_person', ['uuid'], ['uuid'])

  op.drop_constraint(None, 'mds_person_instl_email_addr', type_='foreignkey')
  op.create_foreign_key('SYS_C00281486', 'mds_person_instl_email_addr', 'mds_person', ['uuid'], ['uuid'])

  op.drop_constraint(None, 'mds_person_internet_id', type_='foreignkey')
  op.create_foreign_key('SYS_C00281488', 'mds_person_internet_id', 'mds_person', ['uuid'], ['uuid'])

  op.drop_constraint(None, 'mds_person_last_name', type_='foreignkey')
  op.create_foreign_key('SYS_C00281492', 'mds_person_last_name', 'mds_person', ['uuid'], ['uuid'])

  op.drop_constraint(None, 'mds_person_middle_name', type_='foreignkey')
  op.create_foreign_key('SYS_C00281494', 'mds_person_middle_name', 'mds_person', ['uuid'], ['uuid'])

  op.drop_constraint(None, 'mds_person_name_suffix', type_='foreignkey')
  op.create_foreign_key('SYS_C00281496', 'mds_person_name_suffix', 'mds_person', ['uuid'], ['uuid'])

  op.drop_constraint(None, 'mds_person_preferred_name', type_='foreignkey')
  op.create_foreign_key('SYS_C00281498', 'mds_person_preferred_name', 'mds_person', ['uuid'], ['uuid'])

  op.drop_constraint(None, 'mds_person_primary_empl_rcdno', type_='foreignkey')
  op.create_foreign_key('SYS_C00281500', 'mds_person_primary_empl_rcdno', 'mds_person', ['uuid'], ['uuid'])

  op.drop_constraint(None, 'mds_person_scival_id', type_='foreignkey')
  op.create_foreign_key('SYS_C00281400', 'mds_person_scival_id', 'mds_person', ['uuid'], ['uuid'])

  op.drop_constraint(None, 'mds_person_tenure_flag', type_='foreignkey')
  op.create_foreign_key('SYS_C00281502', 'mds_person_tenure_flag', 'mds_person', ['uuid'], ['uuid'])

  op.drop_constraint(None, 'mds_person_tenure_track_flag', type_='foreignkey')
  op.create_foreign_key('SYS_C00281504', 'mds_person_tenure_track_flag', 'mds_person', ['uuid'], ['uuid'])
