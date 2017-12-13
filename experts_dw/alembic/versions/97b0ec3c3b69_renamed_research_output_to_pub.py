"""Renamed research_output to pub.

Revision ID: 97b0ec3c3b69
Revises: 8c021de5ab1e
Create Date: 2017-05-06 09:15:51.591938

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '97b0ec3c3b69'
down_revision = '8c021de5ab1e'
branch_labels = None
depends_on = None

def upgrade():
  op.rename_table('research_output', 'pub')

def downgrade():
  op.rename_table('pub', 'research_output')
