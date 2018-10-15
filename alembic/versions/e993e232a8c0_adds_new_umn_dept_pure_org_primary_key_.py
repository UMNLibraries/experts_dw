"""Adds new umn_dept_pure_org primary key column: deptid.

Revision ID: e993e232a8c0
Revises: 3197ec6cb8c5
Create Date: 2018-10-15 17:39:04.425147

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'e993e232a8c0'
down_revision = '3197ec6cb8c5'
branch_labels = None
depends_on = None


def upgrade():
  op.drop_constraint('SYS_C00137735', 'umn_dept_pure_org', type_='foreignkey')
  op.drop_constraint('SYS_C00131908', 'umn_dept_pure_org', type_='primary')
  op.add_column('umn_dept_pure_org', sa.Column('deptid', sa.String(length=10)))
  op.execute('UPDATE umn_dept_pure_org SET deptid = TO_CHAR(umn_dept_id)')
  op.create_primary_key(
    'SYS_C00131908',
    'umn_dept_pure_org',
    ['deptid']
  )
  op.create_foreign_key('SYS_C00137735', 'umn_dept_pure_org', 'pure_org', ['pure_org_uuid'], ['pure_uuid'])
  op.alter_column('umn_dept_pure_org', 'umn_dept_name', new_column_name='deptid_descr')


def downgrade():
  op.drop_constraint('SYS_C00137735', 'umn_dept_pure_org', type_='foreignkey')
  op.drop_constraint('SYS_C00131908', 'umn_dept_pure_org', type_='primary')
  op.drop_column('umn_dept_pure_org', 'deptid')
  op.create_primary_key(
    'SYS_C00131908',
    'umn_dept_pure_org',
    ['umn_dept_id']
  )
  op.create_foreign_key('SYS_C00137735', 'umn_dept_pure_org', 'pure_org', ['pure_org_uuid'], ['pure_uuid'])
  op.alter_column('umn_dept_pure_org', 'deptid_descr', new_column_name='umn_dept_name')
