"""Adds job_indicator to PureEligibleEmpJob(New|Previous) PKs.

Revision ID: f81244725381
Revises: 2b4cf6b23dc1
Create Date: 2017-12-23 17:41:58.515501

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'f81244725381'
down_revision = '2b4cf6b23dc1'
branch_labels = None
depends_on = None


def upgrade():
  op.drop_constraint('SYS_C00387275', 'pure_eligible_emp_job_new', type_='primary')
  op.drop_constraint('SYS_C00387279', 'pure_eligible_emp_job_previous', type_='primary')
  op.create_primary_key(
    'SYS_C00387275',
    'pure_eligible_emp_job_new',
    ['emplid','effdt','effseq','position_nbr','jobcode','job_indicator','deptid']
  )
  op.create_primary_key(
    'SYS_C00387279',
    'pure_eligible_emp_job_previous',
    ['emplid','effdt','effseq','position_nbr','jobcode','job_indicator','deptid']
  )

def downgrade():
  op.drop_constraint('SYS_C00387275', 'pure_eligible_emp_job_new', type_='primary')
  op.drop_constraint('SYS_C00387279', 'pure_eligible_emp_job_previous', type_='primary')
  op.create_primary_key(
    'SYS_C00387275',
    'pure_eligible_emp_job_new',
    ['emplid','effdt','effseq','position_nbr','jobcode','deptid']
  )
  op.create_primary_key(
    'SYS_C00387279',
    'pure_eligible_emp_job_previous',
    ['emplid','effdt','effseq','position_nbr','jobcode','deptid']
  )
