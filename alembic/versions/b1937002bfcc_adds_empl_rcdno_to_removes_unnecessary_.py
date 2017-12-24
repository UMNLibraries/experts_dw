"""Adds empl_rcdno to, removes unnecessary columns from PureEligibleEmpJob(New|Previous) PKs.

Revision ID: b1937002bfcc
Revises: f81244725381
Create Date: 2017-12-23 19:24:15.922979

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'b1937002bfcc'
down_revision = 'f81244725381'
branch_labels = None
depends_on = None


def upgrade():
  op.drop_constraint('SYS_C00387275', 'pure_eligible_emp_job_new', type_='primary')
  op.drop_constraint('SYS_C00387279', 'pure_eligible_emp_job_previous', type_='primary')
  op.create_primary_key(
    'SYS_C00387275',
    'pure_eligible_emp_job_new',
    ['emplid','empl_rcdno','effdt','effseq','position_nbr']
  )
  op.create_primary_key(
    'SYS_C00387279',
    'pure_eligible_emp_job_previous',
    ['emplid','empl_rcdno','effdt','effseq','position_nbr']
  )

def downgrade():
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
