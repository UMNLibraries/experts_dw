"""Made pure_internal_org.pure_uuid a FK to pure_org.

Revision ID: ecc2159ed138
Revises: f971a8e94259
Create Date: 2017-05-04 16:25:26.177709

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ecc2159ed138'
down_revision = 'f971a8e94259'
branch_labels = None
depends_on = None

def upgrade():
  op.alter_column(
    'pure_internal_org',
    'pure_uuid',
    existing_type=sa.VARCHAR(length=36),
    nullable=False
  )
  op.create_foreign_key(
    None,
    'pure_internal_org',
    'pure_org',
    ['pure_uuid'],
    ['pure_uuid'],
    ondelete='CASCADE'
  )
  op.drop_column('pure_internal_org', 'type')

def downgrade():
  op.add_column('pure_internal_org', sa.Column('type', sa.VARCHAR(length=25), nullable=True))
  # Probably would need to get the constraint name in order for this to work:
  op.drop_constraint(None, 'pure_internal_org', type_='foreignkey')
  op.alter_column(
    'pure_internal_org',
    'pure_uuid',
    existing_type=sa.VARCHAR(length=36),
    nullable=True
  )
