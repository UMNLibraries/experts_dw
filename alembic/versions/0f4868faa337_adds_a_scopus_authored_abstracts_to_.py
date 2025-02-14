"""Adds a Scopus authored abstracts to download table

Revision ID: 0f4868faa337
Revises: dcc548d3b89b
Create Date: 2024-08-28 13:48:30.215403

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '0f4868faa337'
down_revision = 'dcc548d3b89b'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('scopus_authored_abstracts_to_download',
    sa.Column('scopus_id', sa.Integer(), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('updated_count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('scopus_id', name=op.f('pk_scopus_authored_abstracts_to_download'))
    )

def downgrade():
    op.drop_table('scopus_authored_abstracts_to_download')
