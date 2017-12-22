"""Added pure_org_tree for Pure Organisations.

Revision ID: 1e765500c0f9
Revises: 56540801908b
Create Date: 2017-04-16 17:42:51.093136

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1e765500c0f9'
down_revision = '56540801908b'
branch_labels = None
depends_on = None

def upgrade():
  op.create_table('pure_org_tree',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('type', sa.String(length=25), nullable=True),
    sa.Column('name_en', sa.String(length=255), nullable=True),
    sa.Column('tree_id', sa.Integer(), nullable=True),
    sa.Column('rgt', sa.Integer(), nullable=False),
    sa.Column('lft', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.String(length=50), nullable=True),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['pure_org_tree.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
  )
  op.create_index('pure_org_tree_level_idx', 'pure_org_tree', ['level'], unique=False)
  op.create_index('pure_org_tree_lft_idx', 'pure_org_tree', ['lft'], unique=False)
  op.create_index('pure_org_tree_rgt_idx', 'pure_org_tree', ['rgt'], unique=False)

def downgrade():
  op.drop_index('pure_org_tree_rgt_idx', table_name='pure_org_tree')
  op.drop_index('pure_org_tree_lft_idx', table_name='pure_org_tree')
  op.drop_index('pure_org_tree_level_idx', table_name='pure_org_tree')
  op.drop_table('pure_org_tree')
