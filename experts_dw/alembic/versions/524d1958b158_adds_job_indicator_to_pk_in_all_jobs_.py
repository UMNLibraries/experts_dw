"""Adds job_indicator to PK in all_jobs(new|previous).

Revision ID: 524d1958b158
Revises: 650e250965c9
Create Date: 2017-12-17 12:28:16.803523

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '524d1958b158'
down_revision = '650e250965c9'
branch_labels = None
depends_on = None


def upgrade():
  op.drop_constraint('SYS_C00384862', 'all_jobs_new', type_='primary')
  op.create_primary_key('SYS_C00384862', 'all_jobs_new', ['emplid','jobcode','job_indicator','deptid'])
  op.drop_constraint('SYS_C00384866', 'all_jobs_previous', type_='primary')
  op.create_primary_key('SYS_C00384866', 'all_jobs_previous', ['emplid','jobcode','job_indicator','deptid'])

def downgrade():
  op.drop_constraint('SYS_C00384862', 'all_jobs_new', type_='primary')
  op.create_primary_key('SYS_C00384862', 'all_jobs_new', ['emplid','jobcode','deptid'])
  op.drop_constraint('SYS_C00384866', 'all_jobs_previous', type_='primary')
  op.create_primary_key('SYS_C00384866', 'all_jobs_previous', ['emplid','jobcode','deptid'])
