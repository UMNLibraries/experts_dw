"""Expands size of pure_new_staff_dept_defaults.default_profiled.

Revision ID: 7f7265c52336
Revises: bf6b142f108e
Create Date: 2018-01-21 10:30:28.181392

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '7f7265c52336'
down_revision = 'bf6b142f108e'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('pure_new_staff_dept_defaults', 'default_profiled',
               existing_type=sa.VARCHAR(length=3),
               type_=sa.String(length=5),
               existing_nullable=False)

def downgrade():
    op.alter_column('pure_new_staff_dept_defaults', 'default_profiled',
               existing_type=sa.String(length=5),
               type_=sa.VARCHAR(length=3),
               existing_nullable=False)
