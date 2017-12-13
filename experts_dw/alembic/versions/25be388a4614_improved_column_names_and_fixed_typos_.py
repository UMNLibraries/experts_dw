"""Improved column names and fixed typos in umn_dept_pure_org_map.

Revision ID: 25be388a4614
Revises: a4864a963f7f
Create Date: 2017-04-18 09:04:50.426113

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '25be388a4614'
down_revision = 'a4864a963f7f'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_constraint('SYS_C00282183', 'umn_dept_pure_org_map', type_='primary')
  op.drop_column('umn_dept_pure_org_map', 'umn_id')
  op.add_column('umn_dept_pure_org_map', sa.Column('umn_dept_id', sa.Integer(), nullable=False))
  # Did this manually, because for some reason, this failed or just didn't execute:
  sa.PrimaryKeyConstraint('umn_dept_id')

  op.drop_constraint('SYS_C00282184', 'umn_dept_pure_org_map', type_='foreignkey')
  op.drop_column('umn_dept_pure_org_map', 'pure_id')
  op.add_column('umn_dept_pure_org_map', sa.Column('pure_org_id', sa.String(length=50), nullable=False))
  op.create_foreign_key(None, 'umn_dept_pure_org_map', 'pure_org', ['pure_org_id'], ['pure_id'])

  op.drop_column('umn_dept_pure_org_map', 'umn_name')
  op.add_column('umn_dept_pure_org_map', sa.Column('umn_dept_name', sa.String(length=255), nullable=True))

def downgrade():
  op.drop_constraint(None, 'umn_dept_pure_org_map', type_='primary')
  op.drop_column('umn_dept_pure_org_map', 'umn_dept_id')
  op.add_column('umn_dept_pure_org_map', sa.Column('umn_id', oracle.NUMBER(scale=0, asdecimal=False), nullable=False))
  sa.PrimaryKeyConstraint('umn_id')

  op.drop_constraint(None, 'umn_dept_pure_org_map', type_='foreignkey')
  op.drop_column('umn_dept_pure_org_map', 'pure_org_id')
  op.add_column('umn_dept_pure_org_map', sa.Column('pure_id', oracle.NUMBER(scale=0, asdecimal=False), nullable=False))
  op.create_foreign_key('SYS_C00282184', 'umn_dept_pure_org_map', 'pure_org', ['pure_id'], ['pure_id'])

  op.drop_column('umn_dept_pure_org_map', 'umn_dept_name')
  op.add_column('umn_dept_pure_org_map', sa.Column('umn_name', sa.VARCHAR(length=255), nullable=True))
