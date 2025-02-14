"""Adds a Scopus cited abstracts to download table

Revision ID: 1218833a5dbe
Revises: 43932648fc85
Create Date: 2024-10-18 10:53:10.469119

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '1218833a5dbe'
down_revision = '43932648fc85'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('scopus_cited_abstracts_to_download',
    sa.Column('scopus_id', sa.Integer(), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('scopus_id', name=op.f('pk_scopus_cited_abstracts_to_download'))
    )

def downgrade():
    op.drop_table('scopus_cited_abstracts_to_download')
