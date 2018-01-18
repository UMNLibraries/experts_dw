"""Adds jobcode_descr to pure_new_staff_dept_defaults pk.

Revision ID: 0c70ca64427f
Revises: 13bf6b641fcb
Create Date: 2018-01-18 11:18:24.701486

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '0c70ca64427f'
down_revision = '13bf6b641fcb'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_constraint(
    'SYS_C00394480',
    'pure_new_staff_dept_defaults',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00394480',
    'pure_new_staff_dept_defaults',
    ['deptid', 'jobcode', 'jobcode_descr']
  )

def downgrade():
  op.drop_constraint(
    'SYS_C00394480',
    'pure_new_staff_dept_defaults',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00394480',
    'pure_new_staff_dept_defaults',
    ['deptid', 'jobcode']
  )
