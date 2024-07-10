"""Removes dept-based profiled (PRS) overrides

Revision ID: 01f5d5168215
Revises: 766a087c859b
Create Date: 2024-07-10 08:35:33.810803

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '01f5d5168215'
down_revision = '766a087c859b'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('known_overrideable_employee_jobcode_dept')
    op.drop_table('pure_employee_jobcode_default_override')
    op.drop_column('pure_eligible_employee_jobcode', 'default_profiled_overrideable')

def downgrade():
    op.add_column('pure_eligible_employee_jobcode', sa.Column('default_profiled_overrideable', sa.INTEGER(), nullable=False))

    op.create_table('pure_employee_jobcode_default_override',
    sa.Column('jobcode', sa.VARCHAR(length=13), nullable=False),
    sa.Column('deptid', sa.VARCHAR(length=10), nullable=False),
    sa.Column('profiled', sa.INTEGER(), nullable=False),
    sa.CheckConstraint('profiled IN (0, 1)', name='ck_pure_employee_jobcode_default_override_profiled_bool'),
    sa.PrimaryKeyConstraint('jobcode', 'deptid', name='pk_pure_jobcode_default_override')
    )

    op.create_table('known_overrideable_employee_jobcode_dept',
    sa.Column('jobcode', sa.VARCHAR(length=13), nullable=False),
    sa.Column('deptid', sa.VARCHAR(length=10), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('jobcode', 'deptid', name='pk_known_overrideable_jobcode_dept')
    )
