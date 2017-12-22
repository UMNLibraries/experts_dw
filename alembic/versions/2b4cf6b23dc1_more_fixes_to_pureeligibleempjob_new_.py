"""More fixes to PureEligibleEmpJob(New|Previous) PKs.

Revision ID: 2b4cf6b23dc1
Revises: 688754b0ff43
Create Date: 2017-12-22 17:24:11.900463

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '2b4cf6b23dc1'
down_revision = '688754b0ff43'
branch_labels = None
depends_on = None


def upgrade():
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

def downgrade():
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
