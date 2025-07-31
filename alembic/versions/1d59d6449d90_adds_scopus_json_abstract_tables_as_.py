"""Adds scopus_json_abstract* tables, as part of renaming

Revision ID: 1d59d6449d90
Revises: 1218833a5dbe
Create Date: 2025-07-10 11:39:21.540060

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '1d59d6449d90'
down_revision = '1218833a5dbe'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('scopus_abstracts_to_download',
    sa.Column('scopus_id', sa.Integer(), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('scopus_id', name=op.f('pk_scopus_abstracts_to_download'))
    )
    op.create_table('scopus_json_abstract',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('scopus_id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('scopus_created', sa.DateTime(), nullable=False),
    sa.Column('scopus_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_scopus_json_abstract_json_document')),
    sa.PrimaryKeyConstraint('scopus_id', name=op.f('pk_scopus_json_abstract'))
    )
    op.create_table('scopus_json_abstract_staging',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('scopus_id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('scopus_created', sa.DateTime(), nullable=False),
    sa.Column('scopus_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_scopus_json_abstract_staging_json_document')),
    sa.PrimaryKeyConstraint('scopus_id', 'scopus_modified', name=op.f('pk_scopus_json_abstract_staging'))
    )

def downgrade():
    op.drop_table('scopus_json_abstract_staging')
    op.drop_table('scopus_json_abstract')
    op.drop_table('scopus_abstracts_to_download')
