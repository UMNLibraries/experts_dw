"""Put an index and additional constraints on pub.pure_uuid.

Revision ID: 450247a9a721
Revises: b10d81ad78f2
Create Date: 2017-05-08 15:17:01.999626

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '450247a9a721'
down_revision = 'b10d81ad78f2'
branch_labels = None
depends_on = None

def upgrade():
  op.alter_column(
    'pub',
    'pure_uuid',
    existing_type=sa.VARCHAR(length=36),
    nullable=False
  )
  op.create_index(op.f('ix_pub_pure_uuid'), 'pub', ['pure_uuid'], unique=True)

def downgrade():
  op.drop_index(op.f('ix_pub_pure_uuid'), table_name='pub')
  op.alter_column(
    'pub',
    'pure_uuid',
    existing_type=sa.VARCHAR(length=36),
    nullable=True
  )
