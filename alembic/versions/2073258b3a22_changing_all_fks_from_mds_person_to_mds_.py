"""Changing all FKs from mds_person to mds_person_emplid.

Revision ID: 2073258b3a22
Revises: 85d25911adf2
Create Date: 2017-04-13 15:47:02.929999

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2073258b3a22'
down_revision = '85d25911adf2'
branch_labels = None
depends_on = None


def upgrade():
  op.drop_constraint('SYS_C00264297', 'mds_person_first_name', type_='foreignkey')
  op.create_foreign_key(None, 'mds_person_first_name', 'mds_person_emplid', ['emplid'], ['emplid'])
  op.drop_constraint('SYS_C00264301', 'mds_person_instl_email_addr', type_='foreignkey')
  op.create_foreign_key(None, 'mds_person_instl_email_addr', 'mds_person_emplid', ['emplid'], ['emplid'])
  op.drop_constraint('SYS_C00264305', 'mds_person_internet_id', type_='foreignkey')
  op.create_foreign_key(None, 'mds_person_internet_id', 'mds_person_emplid', ['emplid'], ['emplid'])
  op.drop_constraint('SYS_C00264309', 'mds_person_last_name', type_='foreignkey')
  op.create_foreign_key(None, 'mds_person_last_name', 'mds_person_emplid', ['emplid'], ['emplid'])
  op.drop_constraint('SYS_C00264313', 'mds_person_middle_name', type_='foreignkey')
  op.create_foreign_key(None, 'mds_person_middle_name', 'mds_person_emplid', ['emplid'], ['emplid'])
  op.drop_constraint('SYS_C00264317', 'mds_person_name_suffix', type_='foreignkey')
  op.create_foreign_key(None, 'mds_person_name_suffix', 'mds_person_emplid', ['emplid'], ['emplid'])
  op.drop_constraint('SYS_C00264321', 'mds_person_preferred_name', type_='foreignkey')
  op.create_foreign_key(None, 'mds_person_preferred_name', 'mds_person_emplid', ['emplid'], ['emplid'])
  op.drop_constraint('SYS_C00264343', 'mds_person_primary_empl_rcdno', type_='foreignkey')
  op.create_foreign_key(None, 'mds_person_primary_empl_rcdno', 'mds_person_emplid', ['emplid'], ['emplid'])
  op.drop_constraint('SYS_C00264331', 'mds_person_scival_id', type_='foreignkey')
  op.create_foreign_key(None, 'mds_person_scival_id', 'mds_person_emplid', ['emplid'], ['emplid'])
  op.drop_constraint('SYS_C00264335', 'mds_person_tenure_flag', type_='foreignkey')
  op.create_foreign_key(None, 'mds_person_tenure_flag', 'mds_person_emplid', ['emplid'], ['emplid'])
  op.drop_constraint('SYS_C00264339', 'mds_person_tenure_track_flag', type_='foreignkey')
  op.create_foreign_key(None, 'mds_person_tenure_track_flag', 'mds_person_emplid', ['emplid'], ['emplid'])


def downgrade():
  op.drop_constraint(None, 'mds_person_tenure_track_flag', type_='foreignkey')
  op.create_foreign_key('SYS_C00264339', 'mds_person_tenure_track_flag', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_tenure_flag', type_='foreignkey')
  op.create_foreign_key('SYS_C00264335', 'mds_person_tenure_flag', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_scival_id', type_='foreignkey')
  op.create_foreign_key('SYS_C00264331', 'mds_person_scival_id', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_primary_empl_rcdno', type_='foreignkey')
  op.create_foreign_key('SYS_C00264343', 'mds_person_primary_empl_rcdno', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_preferred_name', type_='foreignkey')
  op.create_foreign_key('SYS_C00264321', 'mds_person_preferred_name', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_name_suffix', type_='foreignkey')
  op.create_foreign_key('SYS_C00264317', 'mds_person_name_suffix', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_middle_name', type_='foreignkey')
  op.create_foreign_key('SYS_C00264313', 'mds_person_middle_name', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_last_name', type_='foreignkey')
  op.create_foreign_key('SYS_C00264309', 'mds_person_last_name', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_internet_id', type_='foreignkey')
  op.create_foreign_key('SYS_C00264305', 'mds_person_internet_id', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_instl_email_addr', type_='foreignkey')
  op.create_foreign_key('SYS_C00264301', 'mds_person_instl_email_addr', 'mds_person', ['emplid'], ['emplid'])
  op.drop_constraint(None, 'mds_person_first_name', type_='foreignkey')
  op.create_foreign_key('SYS_C00264297', 'mds_person_first_name', 'mds_person', ['emplid'], ['emplid'])
