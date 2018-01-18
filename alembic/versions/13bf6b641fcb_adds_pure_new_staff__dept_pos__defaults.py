"""Adds pure_new_staff_(dept|pos)_defaults.

Revision ID: 13bf6b641fcb
Revises: 0df1fa99d4cf
Create Date: 2018-01-18 08:31:18.106688

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '13bf6b641fcb'
down_revision = '0df1fa99d4cf'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'pure_new_staff_dept_defaults',
        sa.Column('deptid', sa.String(length=10), nullable=False),
        sa.Column('deptid_descr', sa.String(length=30), nullable=True),
        sa.Column('pure_org_id', sa.String(length=50), nullable=True),
        sa.Column('jobcode', sa.String(length=13), nullable=False),
        sa.Column('jobcode_descr', sa.String(length=35), nullable=True),
        sa.Column('um_college', sa.String(length=20), nullable=True),
        sa.Column('um_college_descr', sa.String(length=30), nullable=True),
        sa.Column('default_visibility', sa.String(length=10), nullable=False),
        sa.Column('default_profiled', sa.String(length=3), nullable=False),
        sa.PrimaryKeyConstraint('deptid', 'jobcode')
    )
    op.create_table(
        'pure_new_staff_pos_defaults',
        sa.Column('jobcode', sa.String(length=13), nullable=False),
        sa.Column('jobcode_descr', sa.String(length=35), nullable=True),
        sa.Column('um_jobcode_group', sa.String(length=8), nullable=True),
        sa.Column('um_jobcode_group_descr', sa.String(length=50), nullable=True),
        sa.Column('default_staff_type', sa.String(length=10), nullable=False),
        sa.Column('default_employed_as', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('jobcode')
    )

def downgrade():
    op.drop_table('pure_new_staff_pos_defaults')
    op.drop_table('pure_new_staff_dept_defaults')
