"""Dropping umn_dept_pure_org_map so I can recreate it.

Revision ID: fe7a8f156b37
Revises: 2866c54dd3c8
Create Date: 2017-04-18 10:20:08.377129

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'fe7a8f156b37'
down_revision = '2866c54dd3c8'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_table('umn_dept_pure_org_map')

def downgrade():
  op.create_table(
    'umn_dept_pure_org_map',
    sa.Column('umn_dept_id', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('pure_org_id', sa.VARCHAR(length=50), nullable=False),
    sa.Column('umn_dept_name', sa.VARCHAR(length=255), nullable=True),
    sa.ForeignKeyConstraint(['pure_org_id'], ['pure_org.pure_id'], name='SYS_C00282306')
  )
