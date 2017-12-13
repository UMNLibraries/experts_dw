"""Added cascade on delete to all FKs.

Revision ID: b61362caeab4
Revises: 66d69988133c
Create Date: 2017-04-14 16:03:52.376922

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b61362caeab4'
down_revision = '66d69988133c'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_constraint('SYS_C00281356', 'mds_person_instl_email_addr', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_instl_email_addr',
    'mds_person_emplid',
    ['emplid'],
    ['emplid'],
    ondelete='CASCADE'
  )
  op.drop_constraint('SYS_C00281357', 'mds_person_internet_id', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_internet_id',
    'mds_person_emplid',
    ['emplid'],
    ['emplid'],
    ondelete='CASCADE'
  )
  op.drop_constraint('SYS_C00281358', 'mds_person_last_name', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_last_name',
    'mds_person_emplid',
    ['emplid'],
    ['emplid'],
    ondelete='CASCADE'
  )
  op.drop_constraint('SYS_C00281359', 'mds_person_middle_name', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_middle_name',
    'mds_person_emplid',
    ['emplid'],
    ['emplid'],
    ondelete='CASCADE'
  )
  op.drop_constraint('SYS_C00281360', 'mds_person_name_suffix', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_name_suffix',
    'mds_person_emplid',
    ['emplid'],
    ['emplid'],
    ondelete='CASCADE'
  )
  op.drop_constraint('SYS_C00281361', 'mds_person_preferred_name', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_preferred_name',
    'mds_person_emplid',
    ['emplid'],
    ['emplid'],
    ondelete='CASCADE'
  )
  op.drop_constraint('SYS_C00281362', 'mds_person_primary_empl_rcdno', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_primary_empl_rcdno',
    'mds_person_emplid',
    ['emplid'],
    ['emplid'],
    ondelete='CASCADE'
  )
  op.drop_constraint('SYS_C00281363', 'mds_person_scival_id', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_scival_id',
    'mds_person_emplid',
    ['emplid'],
    ['emplid'],
    ondelete='CASCADE'
  )
  op.drop_constraint('SYS_C00281364', 'mds_person_tenure_flag', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_tenure_flag',
    'mds_person_emplid',
    ['emplid'],
    ['emplid'],
    ondelete='CASCADE'
  )
  op.drop_constraint('SYS_C00281365', 'mds_person_tenure_track_flag', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_tenure_track_flag',
    'mds_person_emplid',
    ['emplid'],
    ['emplid'],
    ondelete='CASCADE'
  )

def downgrade():
  op.drop_constraint(None, 'mds_person_tenure_track_flag', type_='foreignkey')
  op.create_foreign_key('SYS_C00281365', 'mds_person_tenure_track_flag', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_tenure_flag', type_='foreignkey')
  op.create_foreign_key('SYS_C00281364', 'mds_person_tenure_flag', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_scival_id', type_='foreignkey')
  op.create_foreign_key('SYS_C00281363', 'mds_person_scival_id', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_primary_empl_rcdno', type_='foreignkey')
  op.create_foreign_key('SYS_C00281362', 'mds_person_primary_empl_rcdno', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_preferred_name', type_='foreignkey')
  op.create_foreign_key('SYS_C00281361', 'mds_person_preferred_name', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_name_suffix', type_='foreignkey')
  op.create_foreign_key('SYS_C00281360', 'mds_person_name_suffix', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_middle_name', type_='foreignkey')
  op.create_foreign_key('SYS_C00281359', 'mds_person_middle_name', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_last_name', type_='foreignkey')
  op.create_foreign_key('SYS_C00281358', 'mds_person_last_name', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_internet_id', type_='foreignkey')
  op.create_foreign_key('SYS_C00281357', 'mds_person_internet_id', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_instl_email_addr', type_='foreignkey')
  op.create_foreign_key('SYS_C00281356', 'mds_person_instl_email_addr', 'mds_person', ['emplid'], ['emplid'])
