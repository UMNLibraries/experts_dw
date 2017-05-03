"""Added pure_internal_org.pure_uuid.

Revision ID: 2254ed89c1d8
Revises: e4cea8e0c5a2
Create Date: 2017-05-03 14:57:12.498078

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2254ed89c1d8'
down_revision = 'e4cea8e0c5a2'
branch_labels = None
depends_on = None


def upgrade():
  op.add_column('pure_internal_org', sa.Column('pure_uuid', sa.String(length=36), nullable=True))

def downgrade():
  op.drop_column('pure_internal_org', 'pure_uuid')
