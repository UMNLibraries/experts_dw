"""Removes timestamps from umn_dept and umn_person PKs.

Revision ID: 57c5c0b90b30
Revises: 2d74720bff39
Create Date: 2017-12-14 16:54:00.170670

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '57c5c0b90b30'
down_revision = '2d74720bff39'
branch_labels = None
depends_on = None


def upgrade():
  op.drop_constraint('SYS_C00383727', 'umn_dept', type_='primary')
  op.alter_column('umn_dept', 'timestamp', existing_type=oracle.DATE(), nullable=True)
  op.create_primary_key('SYS_C00383727', 'umn_dept', ['deptid'])

  op.drop_constraint('SYS_C00383118', 'umn_person', type_='primary')
  op.alter_column('umn_person', 'timestamp', existing_type=oracle.DATE(), nullable=True)
  op.create_primary_key('SYS_C00383118', 'umn_person', ['emplid'])

def downgrade():
  op.drop_constraint('SYS_C00383727', 'umn_dept', type_='primary')
  op.alter_column('umn_person', 'timestamp', existing_type=oracle.DATE(), nullable=False) 
  op.create_primary_key('SYS_C00383727', 'umn_dept', ['deptid', 'timestamp'])

  op.drop_constraint('SYS_C00383118', 'umn_person', type_='primary')
  op.alter_column('umn_dept', 'timestamp', existing_type=oracle.DATE(), nullable=False)
  op.create_primary_key('SYS_C00383118', 'umn_person', ['emplid', 'timestamp'])
