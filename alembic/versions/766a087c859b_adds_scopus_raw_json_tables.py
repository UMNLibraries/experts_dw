"""Adds Scopus raw JSON tables

Revision ID: 766a087c859b
Revises: 2c53d6724ec6
Create Date: 2024-05-14 13:45:39.266564

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '766a087c859b'
down_revision = '2c53d6724ec6'
branch_labels = None
depends_on = None


def upgrade():
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
    op.create_table('scopus_json_collection_meta',
    sa.Column('api_name', sa.String(length=255), nullable=False, comment='Name of the collection in the Scoppus API, i.e., in URL endpoints.'),
    sa.Column('schema_record_name', sa.String(length=255), nullable=False, comment='Name of the collection in API response records.'),
    sa.Column('local_name', sa.String(length=255), nullable=False, comment='Name of the collection as it appears in local table names.'),
    sa.PrimaryKeyConstraint('api_name', 'schema_record_name', 'local_name', name=op.f('pk_scopus_json_collection_meta')),
    comment='Maps Scopus API collection names and JSON schema record names to local table names.'
    )

def downgrade():
    op.drop_table('scopus_json_collection_meta')
    op.drop_table('scopus_json_abstract_staging')
    op.drop_table('scopus_json_abstract')
