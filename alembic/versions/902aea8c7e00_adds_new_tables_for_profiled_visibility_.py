"""Adds new tables for profiled/visibility settings. Attempts to use constraint naming convention.

Revision ID: 902aea8c7e00
Revises: 7b8a16385f5a
Create Date: 2019-02-20 14:05:09.113574

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '902aea8c7e00'
down_revision = '7b8a16385f5a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_eligible_jobcode',
    sa.Column('jobcode', sa.String(length=13), nullable=False),
    sa.Column('jobcode_descr', sa.String(length=35), nullable=True),
    sa.Column('pure_job_description', sa.String(length=50), nullable=False),
    sa.Column('default_employed_as', sa.String(length=50), nullable=False),
    sa.Column('default_staff_type', sa.String(length=11), nullable=False),
    sa.Column('default_visibility', sa.String(length=10), nullable=False),
    sa.Column('default_profiled', sa.Boolean(), nullable=False),
    sa.Column('default_profiled_overrideable', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('jobcode', name=op.f('pk_pure_eligible_jobcode'))
    )
    op.create_table('pure_eligible_affiliate_jobcode',
    sa.Column('jobcode', sa.String(length=13), nullable=False),
    sa.PrimaryKeyConstraint('jobcode', name=op.f('pk_pure_eligible_affiliate_jobcode'))
    )
    op.create_table('pure_eligible_affiliate_dept',
    sa.Column('deptid', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('deptid', name=op.f('pk_pure_eligible_affiliate_dept'))
    )
    op.create_table('pure_jobcode_default_override',
    sa.Column('jobcode', sa.String(length=13), nullable=False),
    sa.Column('deptid', sa.String(length=10), nullable=False),
    sa.Column('profiled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('jobcode', 'deptid', name=op.f('pk_pure_jobcode_default_override'))
    )
    op.create_table('known_overrideable_jobcode_dept',
    sa.Column('jobcode', sa.String(length=13), nullable=False),
    sa.Column('deptid', sa.String(length=10), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('jobcode', 'deptid', name=op.f('pk_known_overrideable_jobcode_dept'))
    )


def downgrade():
    op.drop_table('pure_eligible_jobcode')
    op.drop_table('pure_eligible_affiliate_jobcode')
    op.drop_table('pure_eligible_affiliate_dept')
    op.drop_table('pure_jobcode_default_override')
    op.drop_table('known_overrideable_jobcode_dept')
