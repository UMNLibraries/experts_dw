"""Removes now unused scopus abstract cited tables

Revision ID: 053d0ff8e6a6
Revises: 39e4bca6f097
Create Date: 2025-10-24 13:12:32.591542

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '053d0ff8e6a6'
down_revision = '39e4bca6f097'
branch_labels = None
depends_on = None

def upgrade():
    op.drop_table('scopus_cited_abstracts_to_download')
    op.drop_table('scopus_json_abstract_cited')
    op.drop_table('scopus_json_abstract_cited_staging')

def downgrade():
    op.create_table('scopus_json_abstract_cited_staging',
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('scopus_id', sa.INTEGER(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('scopus_created', oracle.DATE(), nullable=False),
    sa.Column('scopus_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_scopus_json_abstract_cited_staging_json_document'),
    sa.PrimaryKeyConstraint('scopus_id', 'scopus_modified', name='pk_scopus_json_abstract_cited_staging')
    )
    op.create_table('scopus_json_abstract_cited',
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('scopus_id', sa.INTEGER(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('scopus_created', oracle.DATE(), nullable=False),
    sa.Column('scopus_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_scopus_json_abstract_cited_json_document'),
    sa.PrimaryKeyConstraint('scopus_id', name='pk_scopus_json_abstract_cited')
    )
    op.create_table('scopus_cited_abstracts_to_download',
    sa.Column('scopus_id', sa.INTEGER(), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('scopus_id', name='pk_scopus_cited_abstracts_to_download')
    )
