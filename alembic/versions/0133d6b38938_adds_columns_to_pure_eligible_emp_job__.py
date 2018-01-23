"""Adds columns to pure_eligible_emp_job_(new|chng_hst) pks.

Revision ID: 0133d6b38938
Revises: 10fc42d665cc
Create Date: 2018-01-22 15:33:53.884435

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '0133d6b38938'
down_revision = '10fc42d665cc'
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

def downgrade():
  op.drop_constraint(
    'SYS_C00387275',
    'pure_eligible_emp_job_new',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00387275',
    'pure_eligible_emp_job_new',
    ['emplid', 'empl_rcdno', 'effdt', 'effseq', 'position_nbr']
  )
  op.drop_constraint(
    'SYS_C00387279',
    'pure_eligible_emp_job_chng_hst',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00387279',
    'pure_eligible_emp_job_chng_hst',
    ['emplid', 'empl_rcdno', 'effdt', 'effseq', 'position_nbr']
  )
