"""Adds/updates some scopus-json-related tables

Revision ID: a939db178cec
Revises: d1253addfd46
Create Date: 2025-08-05 13:15:16.362671

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'a939db178cec'
down_revision = 'd1253addfd46'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('scopus_abstract_defunct',
    sa.Column('scopus_id', sa.Integer(), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('scopus_id', name=op.f('pk_scopus_abstract_defunct'))
    )
    op.create_table('scopus_abstract_to_download',
    sa.Column('scopus_id', sa.Integer(), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('scopus_id', name=op.f('pk_scopus_abstract_to_download'))
    )
    op.create_table('scopus_citation_defunct',
    sa.Column('scopus_id', sa.Integer(), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('scopus_id', name=op.f('pk_scopus_citation_defunct'))
    )
    op.create_table('scopus_citation_to_download',
    sa.Column('scopus_id', sa.Integer(), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('scopus_id', name=op.f('pk_scopus_citation_to_download'))
    )

def downgrade():
    op.drop_table('scopus_citation_to_download')
    op.drop_table('scopus_citation_defunct')
    op.drop_table('scopus_abstract_to_download')
    op.drop_table('scopus_abstract_defunct')
