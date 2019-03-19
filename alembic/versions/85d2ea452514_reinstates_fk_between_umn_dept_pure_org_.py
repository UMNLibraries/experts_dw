"""Reinstates FK between umn_dept_pure_org and pure_org.

Revision ID: 85d2ea452514
Revises: 53cd97e29673
Create Date: 2019-03-19 14:02:14.885353

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '85d2ea452514'
down_revision = '53cd97e29673'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('umn_dept_pure_org', 'pure_org_uuid',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=36),
               nullable=False)
    op.create_foreign_key(None, 'umn_dept_pure_org', 'pure_org', ['pure_org_uuid'], ['pure_uuid'])

def downgrade():
    op.drop_constraint(None, 'umn_dept_pure_org', type_='foreignkey')
    op.alter_column('umn_dept_pure_org', 'pure_org_uuid',
               existing_type=sa.String(length=36),
               type_=sa.VARCHAR(length=255),
               nullable=True)
