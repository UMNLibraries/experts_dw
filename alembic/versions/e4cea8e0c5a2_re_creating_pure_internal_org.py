"""Re-creating pure_internal_org.

Revision ID: e4cea8e0c5a2
Revises: fd1239632c06
Create Date: 2017-05-03 09:22:20.307758

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e4cea8e0c5a2'
down_revision = 'fd1239632c06'
branch_labels = None
depends_on = None

def upgrade():
  pure_internal_org = op.create_table(
    'pure_internal_org',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pure_id', sa.String(length=50), nullable=True),
    sa.Column('type', sa.String(length=25), nullable=True),
    sa.Column('name_en', sa.String(length=255), nullable=True),
    sa.Column('lft', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('rgt', sa.Integer(), nullable=False),
    sa.Column('tree_id', sa.Integer(), nullable=True),
  )

  # Add data *before* creating all the constraints and indices:
  conn = op.get_bind()
  # Because "level" is an Oracle reserved word, we select *, even though it's fragile.
  # Otherwise, we get confusing errors like: "ORA-01788: CONNECT BY clause required in this query block"
  res = conn.execute('select * from pure_org')
  results = res.fetchall()
  print(results)
  orgs = [{'id': int(r[0]), 'pure_id': r[1], 'type': r[2], 'name_en': r[3], 'parent_id': (int(r[4]) if r[4] is not None else r[4]), 'lft': int(r[5]), 'rgt': int(r[6]), 'level': int(r[7]), 'tree_id': (int(r[8]) if r[8] is not None else r[8])} for r in results]
  op.bulk_insert(pure_internal_org, orgs)

  # *Now* create the constraints and indices:
  #sa.PrimaryKeyConstraint('id')
  op.create_primary_key(None, 'pure_internal_org', ['id'])
  #sa.ForeignKeyConstraint(['parent_id'], ['pure_internal_org.id'], ondelete='CASCADE'),
  op.create_foreign_key(None, 'pure_internal_org', 'pure_internal_org', ['parent_id'], ['id'], ondelete='CASCADE'),

  op.create_index(op.f('ix_pure_internal_org_pure_id'), 'pure_internal_org', ['pure_id'], unique=False)
  op.create_index('pure_internal_org_level_idx', 'pure_internal_org', ['level'], unique=False)
  op.create_index('pure_internal_org_lft_idx', 'pure_internal_org', ['lft'], unique=False)
  op.create_index('pure_internal_org_rgt_idx', 'pure_internal_org', ['rgt'], unique=False)

def downgrade():
  op.drop_index('pure_internal_org_rgt_idx', table_name='pure_internal_org')
  op.drop_index('pure_internal_org_lft_idx', table_name='pure_internal_org')
  op.drop_index('pure_internal_org_level_idx', table_name='pure_internal_org')
  op.drop_index(op.f('ix_pure_internal_org_pure_id'), table_name='pure_internal_org')
  op.drop_table('pure_internal_org')
