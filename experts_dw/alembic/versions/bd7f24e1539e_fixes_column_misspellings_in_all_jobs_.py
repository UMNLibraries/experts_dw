"""Fixes column misspellings in all_jobs_new and all_jobs_previous.

Revision ID: bd7f24e1539e
Revises: abde4ff2e0e1
Create Date: 2017-12-15 17:01:34.497460

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'bd7f24e1539e'
down_revision = 'abde4ff2e0e1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('all_jobs_new', sa.Column('empl_status', sa.String(length=4), nullable=True))
    op.alter_column('all_jobs_new', 'empl_rcdno',
      existing_type=sa.VARCHAR(length=4),
      type_=sa.String(length=40),
      existing_nullable=True)
    op.add_column('all_jobs_previous', sa.Column('empl_status', sa.String(length=4), nullable=True))
    op.alter_column('all_jobs_previous', 'empl_rcdno',
      existing_type=sa.VARCHAR(length=4),
      type_=sa.String(length=40),
      existing_nullable=True)

def downgrade():
    op.alter_column('all_jobs_previous', 'empl_rcdno',
               existing_type=sa.String(length=40),
               type_=sa.VARCHAR(length=4),
               existing_nullable=True)
    op.drop_column('all_jobs_previous', 'empl_status')
    op.alter_column('all_jobs_new', 'empl_rcdno',
               existing_type=sa.String(length=40),
               type_=sa.VARCHAR(length=4),
               existing_nullable=True)
    op.drop_column('all_jobs_new', 'empl_status')
