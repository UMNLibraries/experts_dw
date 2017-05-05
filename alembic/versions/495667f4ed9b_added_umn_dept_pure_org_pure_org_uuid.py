"""Added umn_dept_pure_org.pure_org_uuid.

Revision ID: 495667f4ed9b
Revises: 9de55a132ba4
Create Date: 2017-05-05 08:10:11.863635

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '495667f4ed9b'
down_revision = '9de55a132ba4'
branch_labels = None
depends_on = None

def upgrade():
  op.add_column('umn_dept_pure_org', sa.Column('pure_org_uuid', sa.String(length=36), nullable=True))

def downgrade():
  op.drop_column('umn_dept_pure_org', 'pure_org_uuid')
