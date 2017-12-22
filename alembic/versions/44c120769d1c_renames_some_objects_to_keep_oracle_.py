"""Renames some objects to keep Oracle happy.

Revision ID: 44c120769d1c
Revises: 592fb83a2937
Create Date: 2017-12-22 15:06:28.526525

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '44c120769d1c'
down_revision = '592fb83a2937'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('pure_eligible_emp_job_new', sa.Column('effseq', sa.Integer(), nullable=False))
    op.add_column('pure_eligible_emp_job_new', sa.Column('position_nbr', sa.String(length=8), nullable=False))
    op.add_column('pure_eligible_emp_job_previous', sa.Column('effseq', sa.Integer(), nullable=False))
    op.add_column('pure_eligible_emp_job_previous', sa.Column('position_nbr', sa.String(length=8), nullable=False))

def downgrade():
    op.drop_column('pure_eligible_emp_job_previous', 'position_nbr')
    op.drop_column('pure_eligible_emp_job_previous', 'effseq')
    op.drop_column('pure_eligible_emp_job_new', 'position_nbr')
    op.drop_column('pure_eligible_emp_job_new', 'effseq')
