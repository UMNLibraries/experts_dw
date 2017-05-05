"""Added umn_person_pure_org.pure_org_uuid.

Revision ID: 85f1f3068080
Revises: b23d686156d9
Create Date: 2017-05-05 09:08:02.060925

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '85f1f3068080'
down_revision = 'b23d686156d9'
branch_labels = None
depends_on = None

def upgrade():
  op.add_column('umn_person_pure_org', sa.Column('pure_org_uuid', sa.String(length=36), nullable=True))

def downgrade():
  op.drop_column('umn_person_pure_org', 'pure_org_uuid')
