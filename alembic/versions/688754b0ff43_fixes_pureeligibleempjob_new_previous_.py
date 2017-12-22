"""Fixes PureEligibleEmpJob(New|Previous) PKs.

Revision ID: 688754b0ff43
Revises: 44c120769d1c
Create Date: 2017-12-22 16:57:22.644084

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '688754b0ff43'
down_revision = '44c120769d1c'
branch_labels = None
depends_on = None


def upgrade():
  op.drop_constraint('SYS_C00387275', 'pure_eligible_emp_job_new', type_='primary')
  op.drop_constraint('SYS_C00387279', 'pure_eligible_emp_job_previous', type_='primary')
  op.create_primary_key(
    'SYS_C00387275',
    'pure_eligible_emp_job_new',
    ['emplid','effdt','effseq','position_nbr']
  )
  op.create_primary_key(
    'SYS_C00387279',
    'pure_eligible_emp_job_previous',
    ['emplid','effdt','effseq','position_nbr']
  )

def downgrade():
  op.drop_constraint('SYS_C00387275', 'pure_eligible_emp_job_new', type_='primary')
  op.drop_constraint('SYS_C00387279', 'pure_eligible_emp_job_previous', type_='primary')
  op.create_primary_key(
    'SYS_C00387275',
    'pure_eligible_emp_job_new',
    ['emplid','effdt','deptid']
  )
  op.create_primary_key(
    'SYS_C00387279',
    'pure_eligible_emp_job_previous',
    ['emplid','effdt','deptid']
  )
