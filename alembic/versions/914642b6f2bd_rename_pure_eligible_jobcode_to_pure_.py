"""rename pure_eligible_jobcode to pure_eligible_employee_jobcode

Revision ID: 914642b6f2bd
Revises: 272054f1c058
Create Date: 2019-09-19 12:03:05.879197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '914642b6f2bd'
down_revision = '272054f1c058'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('pure_eligible_jobcode', 'pure_eligible_employee_jobcode')
    op.rename_table('known_overrideable_jobcode_dept', 'known_overrideable_employee_jobcode_dept')
    op.rename_table('pure_jobcode_default_override', 'pure_employee_jobcode_default_override')


def downgrade():
    op.rename_table('pure_eligible_employee_jobcode', 'pure_eligible_jobcode')
    op.rename_table('known_overrideable_employee_jobcode_dept', 'known_overrideable_jobcode_dept')
    op.rename_table('pure_employee_jobcode_default_override', 'pure_jobcode_default_override')
