"""Added remaining columns to pure_org.

Revision ID: f971a8e94259
Revises: 890ad383d634
Create Date: 2017-05-04 13:36:15.675066

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f971a8e94259'
down_revision = '890ad383d634'
branch_labels = None
depends_on = None

def upgrade():
  op.create_table(
    'pure_org',
    sa.Column('pure_uuid', sa.String(length=36), nullable=False),
    sa.Column('pure_id', sa.String(length=50), nullable=True),
    sa.Column('parent_pure_uuid', sa.String(length=36), nullable=True),
    sa.Column('parent_pure_id', sa.String(length=50), nullable=True),
    sa.Column('pure_internal', sa.String(length=1), nullable=False),
    sa.Column('type', sa.String(length=25), nullable=True),
    sa.Column('name_en', sa.String(length=255), nullable=False),
    sa.Column('name_variant_en', sa.String(length=255), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('pure_uuid')
  )

def downgrade():
  op.drop_table('pure_org')
