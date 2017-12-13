"""Removed remaining pure_org.pure_id FKs.

Revision ID: dea9120b5670
Revises: dfc4d651ed31
Create Date: 2017-05-03 15:18:41.802606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dea9120b5670'
down_revision = 'dfc4d651ed31'
branch_labels = None
depends_on = None


def upgrade():
  op.alter_column(
    'umn_dept_pure_org_map',
    'pure_org_id',
    existing_type=sa.VARCHAR(length=50),
    nullable=True
  )
  op.drop_constraint('SYS_C00282317', 'umn_dept_pure_org_map', type_='foreignkey')

def downgrade():
  op.create_foreign_key(
    'SYS_C00282317',
    'umn_dept_pure_org_map',
    'pure_org',
    ['pure_org_id'],
    ['pure_id']
  )
  op.alter_column(
    'umn_dept_pure_org_map',
    'pure_org_id',
    existing_type=sa.VARCHAR(length=50),
    nullable=False
  )
