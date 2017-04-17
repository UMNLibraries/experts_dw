"""Re-creating pure_org.

Revision ID: 3fb5e65aa3de
Revises: 9f257b57fca6
Create Date: 2017-04-16 19:11:49.315481

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3fb5e65aa3de'
down_revision = '9f257b57fca6'
branch_labels = None
depends_on = None

def upgrade():
  op.create_table(
    'pure_org',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pure_id', sa.String(length=50), nullable=False),
    sa.Column('type', sa.String(length=25), nullable=True),
    sa.Column('name_en', sa.String(length=255), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('lft', sa.Integer(), nullable=False),
    sa.Column('rgt', sa.Integer(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('tree_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['pure_org.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('pure_id')
  )
  op.create_index('pure_org_level_idx', 'pure_org', ['level'], unique=False)
  op.create_index('pure_org_lft_idx', 'pure_org', ['lft'], unique=False)
  op.create_index('pure_org_rgt_idx', 'pure_org', ['rgt'], unique=False)

def downgrade():
  op.drop_index('pure_org_rgt_idx', table_name='pure_org')
  op.drop_index('pure_org_lft_idx', table_name='pure_org')
  op.drop_index('pure_org_level_idx', table_name='pure_org')
  op.drop_table('pure_org')
