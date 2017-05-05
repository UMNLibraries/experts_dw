"""Made person.pure_internal not nullable.

Revision ID: f9d0ad353c15
Revises: aa46fdd1c8ec
Create Date: 2017-05-05 12:39:53.509562

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f9d0ad353c15'
down_revision = 'aa46fdd1c8ec'
branch_labels = None
depends_on = None

def upgrade():
  op.alter_column(
    'person',
    'pure_internal',
    existing_type=sa.VARCHAR(length=1),
    nullable=False
  )

def downgrade():
  op.alter_column(
    'person',
    'pure_internal',
    existing_type=sa.VARCHAR(length=1),
    nullable=True
  )
