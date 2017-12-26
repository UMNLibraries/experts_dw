"""More descriptive naming for some tables: changes  _previous to _chng_hst.

Revision ID: 3125317d28a2
Revises: 51a1a5f4da0c
Create Date: 2017-12-26 16:31:53.822833

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '3125317d28a2'
down_revision = '51a1a5f4da0c'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('pure_eligible_aff_job_previous', 'pure_eligible_aff_job_chng_hst')
    op.rename_table('pure_eligible_emp_job_previous', 'pure_eligible_emp_job_chng_hst')

def downgrade():
    op.rename_table('pure_eligible_aff_job_chng_hst', 'pure_eligible_aff_job_previous')
    op.rename_table('pure_eligible_emp_job_chng_hst', 'pure_eligible_emp_job_previous')
