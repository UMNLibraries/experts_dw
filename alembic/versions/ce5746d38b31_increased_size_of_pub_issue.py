"""Increased size of pub.issue.

Revision ID: ce5746d38b31
Revises: 450247a9a721
Create Date: 2017-05-12 04:12:17.795642

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ce5746d38b31'
down_revision = '450247a9a721'
branch_labels = None
depends_on = None

def upgrade():
  op.alter_column(
    'pub',
    'issue',
    existing_type=sa.VARCHAR(length=25),
    type_=sa.String(length=50),
    existing_nullable=True
  )

def downgrade():
  op.alter_column(
    'pub',
    'issue',
    existing_type=sa.String(length=50),
    type_=sa.VARCHAR(length=25),
    existing_nullable=True
  )
