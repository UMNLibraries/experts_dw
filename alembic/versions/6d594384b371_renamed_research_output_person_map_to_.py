"""Renamed research_output_person_map to pub_person.

Revision ID: 6d594384b371
Revises: 97b0ec3c3b69
Create Date: 2017-05-06 09:22:20.400923

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '6d594384b371'
down_revision = '97b0ec3c3b69'
branch_labels = None
depends_on = None

def upgrade():
  op.rename_table('research_output_person_map', 'pub_person')

def downgrade():
  op.rename_table('pub_person', 'research_output_person_map')
