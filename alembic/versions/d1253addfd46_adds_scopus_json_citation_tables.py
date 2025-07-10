"""Adds scopus_json_citation* tables

Revision ID: d1253addfd46
Revises: ef7a41901208
Create Date: 2025-07-10 13:14:51.308602

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'd1253addfd46'
down_revision = 'ef7a41901208'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('scopus_citations_to_download',
    sa.Column('scopus_id', sa.Integer(), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('scopus_id', name=op.f('pk_scopus_citations_to_download'))
    )
    op.create_table('scopus_json_citation',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('scopus_id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('scopus_created', sa.DateTime(), nullable=False),
    sa.Column('scopus_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_scopus_json_citation_json_document')),
    sa.PrimaryKeyConstraint('scopus_id', name=op.f('pk_scopus_json_citation'))
    )
    op.create_table('scopus_json_citation_staging',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('scopus_id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('scopus_created', sa.DateTime(), nullable=False),
    sa.Column('scopus_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_scopus_json_citation_staging_json_document')),
    sa.PrimaryKeyConstraint('scopus_id', 'scopus_modified', name=op.f('pk_scopus_json_citation_staging'))
    )

def downgrade():
    op.drop_table('scopus_json_citation_staging')
    op.drop_table('scopus_json_citation')
    op.drop_table('scopus_citations_to_download')
