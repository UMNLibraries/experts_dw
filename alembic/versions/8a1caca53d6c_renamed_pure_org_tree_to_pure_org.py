"""Renamed pure_org_tree to pure_org.

Revision ID: 8a1caca53d6c
Revises: 1e765500c0f9
Create Date: 2017-04-16 17:57:05.189692

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '8a1caca53d6c'
down_revision = '1e765500c0f9'
branch_labels = None
depends_on = None

def upgrade():
  op.create_table('pure_org',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('type', sa.String(length=25), nullable=True),
    sa.Column('name_en', sa.String(length=255), nullable=True),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('lft', sa.Integer(), nullable=False),
    sa.Column('rgt', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.String(length=50), nullable=True),
    sa.Column('tree_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['pure_org.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
  )
  op.create_index('pure_org_level_idx', 'pure_org', ['level'], unique=False)
  op.create_index('pure_org_lft_idx', 'pure_org', ['lft'], unique=False)
  op.create_index('pure_org_rgt_idx', 'pure_org', ['rgt'], unique=False)
  op.drop_table('pure_org_tree')

def downgrade():
  op.create_table('pure_org_tree',
    sa.Column('id', sa.VARCHAR(length=50), nullable=False),
    sa.Column('type', sa.VARCHAR(length=25), nullable=True),
    sa.Column('name_en', sa.VARCHAR(length=255), nullable=True),
    sa.Column('tree_id', oracle.NUMBER(scale=0, asdecimal=False), nullable=True),
    sa.Column('rgt', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('lft', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('parent_id', sa.VARCHAR(length=50), nullable=True),
    sa.Column('level', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['pure_org_tree.id'], name='SYS_C00281946'),
    sa.PrimaryKeyConstraint('id', name='sys_c00281945')
  )
  op.drop_index('pure_org_rgt_idx', table_name='pure_org')
  op.drop_index('pure_org_lft_idx', table_name='pure_org')
  op.drop_index('pure_org_level_idx', table_name='pure_org')
  op.drop_table('pure_org')
