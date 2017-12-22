"""Makes umn_dept and umn_person timestamps not null.

Revision ID: e640c0411156
Revises: 57c5c0b90b30
Create Date: 2017-12-14 17:37:15.828929

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'e640c0411156'
down_revision = '57c5c0b90b30'
branch_labels = None
depends_on = None


def upgrade():
  op.alter_column('umn_dept', 'timestamp', existing_type=oracle.DATE(), nullable=False)
  op.alter_column('umn_person', 'timestamp', existing_type=oracle.DATE(), nullable=False)

def downgrade():
  op.alter_column('umn_person', 'timestamp', existing_type=oracle.DATE(), nullable=True)
  op.alter_column('umn_dept', 'timestamp', existing_type=oracle.DATE(), nullable=True)
