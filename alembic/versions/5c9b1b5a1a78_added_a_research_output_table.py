"""Added a research_output table.

Revision ID: 5c9b1b5a1a78
Revises: 7555936f7b6c
Create Date: 2017-04-28 15:36:58.200546

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5c9b1b5a1a78'
down_revision = '7555936f7b6c'
branch_labels = None
depends_on = None

def upgrade():
  op.create_table(
    'research_output',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('pure_uuid', sa.String(length=36), nullable=True),
    sa.Column('scopus_id', sa.String(length=35), nullable=True),
    sa.Column('pmid', sa.String(length=50), nullable=True),
    sa.Column('doi', sa.String(length=150), nullable=True),
    sa.Column('type', sa.String(length=50), nullable=True),
    sa.Column('title', sa.String(length=2000), nullable=False),
    sa.Column('container_title', sa.String(length=2000), nullable=True),
    sa.Column('issued', sa.DateTime(), nullable=False),
    sa.Column('issued_precision', sa.Integer(), nullable=False),
    sa.Column('volume', sa.String(length=25), nullable=True),
    sa.Column('issue', sa.String(length=25), nullable=True),
    sa.Column('pages', sa.String(length=50), nullable=True),
    sa.Column('citation_total', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
  )

def downgrade():
  op.drop_table('research_output')
