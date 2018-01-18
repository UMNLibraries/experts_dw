"""Expands size of pure_new_staff_pos_defaults.default_staff_type.

Revision ID: bf6b142f108e
Revises: 0c70ca64427f
Create Date: 2018-01-18 12:04:12.806554

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'bf6b142f108e'
down_revision = '0c70ca64427f'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('pure_new_staff_pos_defaults', 'default_staff_type',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=11),
               existing_nullable=False)

def downgrade():
    op.alter_column('pure_new_staff_pos_defaults', 'default_staff_type',
               existing_type=sa.String(length=11),
               type_=sa.VARCHAR(length=10),
               existing_nullable=False)
