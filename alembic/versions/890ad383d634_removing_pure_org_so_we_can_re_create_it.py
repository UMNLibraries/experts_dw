"""Removing pure_org so we can re-create it.

Revision ID: 890ad383d634
Revises: dea9120b5670
Create Date: 2017-05-03 15:25:42.938136

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '890ad383d634'
down_revision = 'dea9120b5670'
branch_labels = None
depends_on = None


def upgrade():
  op.drop_table('pure_org')


def downgrade():
  op.create_table(
    'pure_org',
    sa.Column('id', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('pure_id', sa.VARCHAR(length=50), nullable=False),
    sa.Column('type', sa.VARCHAR(length=25), nullable=True),
    sa.Column('name_en', sa.VARCHAR(length=255), nullable=True),
    sa.Column('parent_id', oracle.NUMBER(scale=0, asdecimal=False), nullable=True),
    sa.Column('lft', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('rgt', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('level', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('tree_id', oracle.NUMBER(scale=0, asdecimal=False), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['pure_org.id'], name='SYS_C00281980'),
    sa.PrimaryKeyConstraint('id', name='sys_c00281978')
  )
