"""Adds more columns to pure_eligible_emp_job_(new|chng_hst) pks.

Revision ID: a96a3b78b47b
Revises: 0133d6b38938
Create Date: 2018-01-22 15:48:52.964823

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'a96a3b78b47b'
down_revision = '0133d6b38938'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_constraint(
    'SYS_C00387275',
    'pure_eligible_emp_job_new',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00387275',
    'pure_eligible_emp_job_new',
    ['emplid', 'empl_rcdno', 'effdt', 'effseq', 'position_nbr', 'empl_status', 'status_flg', 'jobcode', 'deptid']
  )
  op.drop_constraint(
    'SYS_C00387279',
    'pure_eligible_emp_job_chng_hst',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00387279',
    'pure_eligible_emp_job_chng_hst',
    ['emplid', 'empl_rcdno', 'effdt', 'effseq', 'position_nbr', 'empl_status', 'status_flg', 'jobcode', 'deptid']
  )

def downgrade():
  op.drop_constraint(
    'SYS_C00387275',
    'pure_eligible_emp_job_new',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00387275',
    'pure_eligible_emp_job_new',
    ['emplid', 'empl_rcdno', 'effdt', 'effseq', 'position_nbr', 'empl_status', 'status_flg']
  )
  op.drop_constraint(
    'SYS_C00387279',
    'pure_eligible_emp_job_chng_hst',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00387279',
    'pure_eligible_emp_job_chng_hst',
    ['emplid', 'empl_rcdno', 'effdt', 'effseq', 'position_nbr', 'empl_status', 'status_flg']
  )
