"""Fixes jobcode length in all_jobs_(new|previous).

Revision ID: 650e250965c9
Revises: bd7f24e1539e
Create Date: 2017-12-17 10:27:45.178095

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '650e250965c9'
down_revision = 'bd7f24e1539e'
branch_labels = None
depends_on = None


def upgrade():
  op.alter_column(
    'all_jobs_new',
    'jobcode',
    existing_type=sa.VARCHAR(length=6),
    type_=sa.String(length=13)
  )
  op.alter_column(
    'all_jobs_previous',
    'jobcode',
    existing_type=sa.VARCHAR(length=6),
    type_=sa.String(length=13)
  )

def downgrade():
  op.alter_column(
    'all_jobs_previous',
    'jobcode',
    existing_type=sa.String(length=13),
    type_=sa.VARCHAR(length=6)
  )
  op.alter_column(
    'all_jobs_new',
    'jobcode',
    existing_type=sa.String(length=13),
    type_=sa.VARCHAR(length=6)
  )
