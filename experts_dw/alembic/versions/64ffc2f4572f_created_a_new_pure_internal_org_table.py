"""Created a new pure_internal_org table.

Revision ID: 64ffc2f4572f
Revises: bc128617ce72
Create Date: 2017-05-02 15:01:54.546361

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '64ffc2f4572f'
down_revision = 'bc128617ce72'
branch_labels = None
depends_on = None

def upgrade():
  op.create_table('pure_internal_org',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pure_uuid', sa.String(length=36), nullable=False),
    sa.Column('pure_id', sa.String(length=50), nullable=True),
    sa.Column('type', sa.String(length=25), nullable=True),
    sa.Column('name_en', sa.String(length=255), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('rgt', sa.Integer(), nullable=False),
    sa.Column('lft', sa.Integer(), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('tree_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['pure_internal_org.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('pure_uuid')
  )
  op.create_index(op.f('ix_pure_internal_org_pure_id'), 'pure_internal_org', ['pure_id'], unique=False)
  op.create_index('pure_internal_org_level_idx', 'pure_internal_org', ['level'], unique=False)
  op.create_index('pure_internal_org_lft_idx', 'pure_internal_org', ['lft'], unique=False)
  op.create_index('pure_internal_org_rgt_idx', 'pure_internal_org', ['rgt'], unique=False)
  op.drop_index('ix_research_output_per_04bc', table_name='research_output_person_map')
  op.create_index(op.f('ix_rsrch_output_persom_emplid'), 'research_output_person_map', ['emplid'], unique=False)

def downgrade():
  op.create_index('ix_research_output_per_04bc', 'research_output_person_map', ['emplid'], unique=False)
  # Will need to get the actual index name, otherwise this will fail:
  op.drop_index(op.f('ix_rsrch_output_persom_emplid'), table_name='research_output_person_map')
  op.drop_index('pure_internal_org_rgt_idx', table_name='pure_internal_org')
  op.drop_index('pure_internal_org_lft_idx', table_name='pure_internal_org')
  op.drop_index('pure_internal_org_level_idx', table_name='pure_internal_org')
  op.drop_index(op.f('ix_pure_internal_org_pure_id'), table_name='pure_internal_org')
  op.drop_table('pure_internal_org')
