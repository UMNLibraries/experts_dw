"""Removing pure_org so I can re-create it correctly.

Revision ID: 9f257b57fca6
Revises: 8a1caca53d6c
Create Date: 2017-04-16 19:10:13.521359

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '9f257b57fca6'
down_revision = '8a1caca53d6c'
branch_labels = None
depends_on = None


def upgrade():
  op.drop_table('pure_org')

def downgrade():
  op.create_table(
    'pure_org',
    sa.Column('id', sa.VARCHAR(length=50), nullable=False),
    sa.Column('type', sa.VARCHAR(length=25), nullable=True),
    sa.Column('name_en', sa.VARCHAR(length=255), nullable=True),
    sa.Column('level', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('lft', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('rgt', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('parent_id', sa.VARCHAR(length=50), nullable=True),
    sa.Column('tree_id', oracle.NUMBER(scale=0, asdecimal=False), nullable=True),
    sa.Column('pure_id', sa.VARCHAR(length=50), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['pure_org.id'], name='SYS_C00281952'),
    sa.PrimaryKeyConstraint('id', name='sys_c00281951')
  )
