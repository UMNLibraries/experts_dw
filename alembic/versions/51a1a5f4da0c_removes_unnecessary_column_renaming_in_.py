"""Removes unnecessary column-renaming in PureEligibleEmpJob(New|Previous)?.

Revision ID: 51a1a5f4da0c
Revises: 3263b202dade
Create Date: 2017-12-25 14:30:07.348359

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '51a1a5f4da0c'
down_revision = '3263b202dade'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('pure_eligible_emp_job_new', 'calculated_start_dt')
    op.drop_column('pure_eligible_emp_job_new', 'campus')
    op.add_column('pure_eligible_emp_job_new', sa.Column('rrc', sa.String(length=20), nullable=True))

    op.drop_column('pure_eligible_emp_job_previous', 'calculated_start_dt')
    op.drop_column('pure_eligible_emp_job_previous', 'campus')
    op.add_column('pure_eligible_emp_job_previous', sa.Column('rrc', sa.String(length=20), nullable=True))


def downgrade():
    op.drop_column('pure_eligible_emp_job_previous', 'rrc')
    op.add_column('pure_eligible_emp_job_previous', sa.Column('campus', sa.VARCHAR(length=20), nullable=True))
    op.add_column('pure_eligible_emp_job_previous', sa.Column('calculated_start_dt', oracle.DATE(), nullable=True))

    op.drop_column('pure_eligible_emp_job_new', 'rrc')
    op.add_column('pure_eligible_emp_job_new', sa.Column('campus', sa.VARCHAR(length=20), nullable=True))
    op.add_column('pure_eligible_emp_job_new', sa.Column('calculated_start_dt', oracle.DATE(), nullable=True))
