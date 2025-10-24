"""Alters data type of remaining scopus_to_download*.scopus_id columns

Revision ID: a98bdea48f7d
Revises: 34f7bacb9553
Create Date: 2025-10-24 09:04:13.130115

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'a98bdea48f7d'
down_revision = '34f7bacb9553'
branch_labels = None
depends_on = None

def upgrade():
    op.execute('ALTER TABLE scopus_abstract_to_download DROP CONSTRAINT pk_scopus_abstract_to_download')
    op.alter_column('scopus_abstract_to_download', 'scopus_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=50),
               existing_nullable=False)
    op.create_primary_key('pk_scopus_abstract_to_download', 'scopus_abstract_to_download', ['scopus_id'])

    op.execute('ALTER TABLE scopus_citation_to_download DROP CONSTRAINT pk_scopus_citation_to_download')
    op.alter_column('scopus_citation_to_download', 'scopus_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=50),
               existing_nullable=False)
    op.create_primary_key('pk_scopus_citation_to_download', 'scopus_citation_to_download', ['scopus_id'])

def downgrade():
    op.execute('ALTER TABLE scopus_citation_to_download DROP CONSTRAINT pk_scopus_citation_to_download')
    op.alter_column('scopus_citation_to_download', 'scopus_id',
               existing_type=sa.String(length=50),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.create_primary_key('pk_scopus_citation_to_download', 'scopus_citation_to_download', ['scopus_id'])

    op.execute('ALTER TABLE scopus_abstract_to_download DROP CONSTRAINT pk_scopus_abstract_to_download')
    op.alter_column('scopus_abstract_to_download', 'scopus_id',
               existing_type=sa.String(length=50),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.create_primary_key('pk_scopus_abstract_to_download', 'scopus_abstract_to_download', ['scopus_id'])
