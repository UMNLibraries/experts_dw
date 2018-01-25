"""Changes pure_eligible_(aff|emp)_job_chng_hst pks to emplid + timestamp.

Revision ID: f4915a36781d
Revises: ea9ae7843c0e
Create Date: 2018-01-23 13:42:12.664825

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'f4915a36781d'
down_revision = 'ea9ae7843c0e'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_constraint(
    'SYS_C00387810',
    'pure_eligible_aff_job_chng_hst',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00387810',
    'pure_eligible_aff_job_chng_hst',
    ['emplid', 'timestamp']
  )
  op.alter_column('pure_eligible_aff_job_chng_hst', 'deptid',
             existing_type=sa.VARCHAR(length=10),
             nullable=True)
  op.alter_column('pure_eligible_aff_job_chng_hst', 'effdt',
             existing_type=oracle.DATE(),
             nullable=True)
  op.alter_column('pure_eligible_aff_job_chng_hst', 'um_affiliate_id',
             existing_type=sa.VARCHAR(length=2),
             nullable=True)

  op.drop_constraint(
    'SYS_C00387279',
    'pure_eligible_emp_job_chng_hst',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00387279',
    'pure_eligible_emp_job_chng_hst',
    ['emplid', 'timestamp']
  )
  op.alter_column('pure_eligible_emp_job_chng_hst', 'effdt',
             existing_type=oracle.DATE(),
             nullable=True)
  op.alter_column('pure_eligible_emp_job_chng_hst', 'effseq',
             existing_type=oracle.NUMBER(scale=0, asdecimal=False),
             nullable=True)
  op.alter_column('pure_eligible_emp_job_chng_hst', 'position_nbr',
             existing_type=sa.VARCHAR(length=8),
             nullable=True)

def downgrade():
  op.drop_constraint(
    'SYS_C00387810',
    'pure_eligible_aff_job_chng_hst',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00387810',
    'pure_eligible_aff_job_chng_hst',
    ['emplid', 'um_affiliate_id', 'effdt', 'deptid']
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
