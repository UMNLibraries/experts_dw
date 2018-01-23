"""Adds timestamps to pure_eligible_(aff|emp)_job_chng_hst.

Revision ID: ea9ae7843c0e
Revises: a96a3b78b47b
Create Date: 2018-01-23 12:10:43.846930

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'ea9ae7843c0e'
down_revision = 'a96a3b78b47b'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('pure_eligible_aff_job_chng_hst', sa.Column('timestamp', sa.DateTime(), nullable=True))
    op.add_column('pure_eligible_emp_job_chng_hst', sa.Column('timestamp', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('pure_eligible_emp_job_chng_hst', 'timestamp')
    op.drop_column('pure_eligible_aff_job_chng_hst', 'timestamp')
