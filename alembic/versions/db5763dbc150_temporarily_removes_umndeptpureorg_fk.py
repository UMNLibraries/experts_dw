"""Temporarily removes UmnDeptPureOrg FK.

Revision ID: db5763dbc150
Revises: 53d7e718c455
Create Date: 2019-03-11 14:25:40.232802

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'db5763dbc150'
down_revision = '53d7e718c455'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('umn_dept_pure_org', 'pure_org_uuid',
               existing_type=sa.VARCHAR(length=36),
               type_=sa.String(length=255),
               nullable=True,
               comment=None,
               existing_comment='Foreign key to PURE_ORG.')
    op.drop_constraint('sys_c00137735', 'umn_dept_pure_org', type_='foreignkey')

def downgrade():
    op.create_foreign_key('sys_c00137735', 'umn_dept_pure_org', 'pure_org', ['pure_org_uuid'], ['pure_uuid'])
    op.alter_column('umn_dept_pure_org', 'pure_org_uuid',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=36),
               nullable=False,
               comment='Foreign key to PURE_ORG.')
