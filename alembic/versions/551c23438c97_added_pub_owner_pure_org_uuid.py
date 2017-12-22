"""Added pub.owner_pure_org_uuid.

Revision ID: 551c23438c97
Revises: 7f24240aabd0
Create Date: 2017-05-08 14:15:45.341812

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '551c23438c97'
down_revision = '7f24240aabd0'
branch_labels = None
depends_on = None

def upgrade():
  op.add_column('pub', sa.Column('owner_pure_org_uuid', sa.String(length=36), nullable=False))
  op.create_foreign_key(
    None,
    'pub',
    'pure_org',
    ['owner_pure_org_uuid'],
    ['pure_uuid'],
    ondelete='CASCADE'
  )

def downgrade():
  # Would need the generated constraint name for this to work:
  op.drop_constraint(None, 'pub', type_='foreignkey')
  op.drop_column('pub', 'owner_pure_org_uuid')
