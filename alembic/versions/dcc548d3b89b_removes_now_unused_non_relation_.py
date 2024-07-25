"""Removes now-unused non-relation-specific Scopus tables

Revision ID: dcc548d3b89b
Revises: 90bc1ffa5a51
Create Date: 2024-07-25 13:46:06.965562

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'dcc548d3b89b'
down_revision = '90bc1ffa5a51'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('scopus_json_abstract')
    op.drop_table('scopus_json_abstract_staging')

def downgrade():
    op.create_table('scopus_json_abstract_staging',
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('scopus_id', sa.INTEGER(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('scopus_created', oracle.DATE(), nullable=False),
    sa.Column('scopus_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_scopus_json_abstract_staging_json_document'),
    sa.PrimaryKeyConstraint('scopus_id', 'scopus_modified', name='pk_scopus_json_abstract_staging')
    )
    op.create_table('scopus_json_abstract',
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('scopus_id', sa.INTEGER(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('scopus_created', oracle.DATE(), nullable=False),
    sa.Column('scopus_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_scopus_json_abstract_json_document'),
    sa.PrimaryKeyConstraint('scopus_id', name='pk_scopus_json_abstract')
    )
