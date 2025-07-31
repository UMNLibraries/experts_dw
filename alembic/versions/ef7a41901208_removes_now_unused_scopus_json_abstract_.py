"""Removes now-unused scopus_json_abstract_authored* tables, as part of renaming

Revision ID: ef7a41901208
Revises: 1d59d6449d90
Create Date: 2025-07-10 13:04:12.030489

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'ef7a41901208'
down_revision = '1d59d6449d90'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('scopus_authored_abstracts_to_download')
    op.drop_table('scopus_json_abstract_authored_staging')
    op.drop_table('scopus_json_abstract_authored')

def downgrade():
    op.create_table('scopus_json_abstract_authored',
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('scopus_id', sa.INTEGER(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('scopus_created', oracle.DATE(), nullable=False),
    sa.Column('scopus_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_scopus_json_abstract_authored_json_document')),
    sa.PrimaryKeyConstraint('scopus_id', name=op.f('pk_scopus_json_abstract_authored'))
    )
    op.create_table('scopus_json_abstract_authored_staging',
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('scopus_id', sa.INTEGER(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('scopus_created', oracle.DATE(), nullable=False),
    sa.Column('scopus_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_scopus_json_abstract_authored_staging_json_document')),
    sa.PrimaryKeyConstraint('scopus_id', 'scopus_modified', name=op.f('pk_scopus_json_abstract_authored_staging'))
    )
    op.create_table('scopus_authored_abstracts_to_download',
    sa.Column('scopus_id', sa.INTEGER(), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('scopus_id', name=op.f('pk_scopus_authored_abstracts_to_download'))
    )
