"""Added a research_output.issn column.

Revision ID: a0ee4912db65
Revises: e7dd66766238
Create Date: 2017-04-29 14:00:19.510567

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a0ee4912db65'
down_revision = 'e7dd66766238'
branch_labels = None
depends_on = None

def upgrade():
  op.add_column('research_output', sa.Column('issn', sa.String(length=9), nullable=True))

def downgrade():
  op.drop_column('research_output', 'issn')
