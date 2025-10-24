"""Alters data type of scopus_*defunct*.scopus_id columns

Revision ID: 39e4bca6f097
Revises: 6a1113139424
Create Date: 2025-10-24 12:27:30.933619

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '39e4bca6f097'
down_revision = '6a1113139424'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('scopus_abstract_defunct', sa.Column('scopus_id_temp', sa.String(50), nullable=True))
    op.execute('UPDATE scopus_abstract_defunct SET scopus_id_temp = TO_CHAR(scopus_id)')
    op.execute('ALTER TABLE scopus_abstract_defunct DROP CONSTRAINT pk_scopus_abstract_defunct')
    op.drop_column('scopus_abstract_defunct', 'scopus_id')
    op.add_column('scopus_abstract_defunct', sa.Column('scopus_id', sa.String(50), nullable=True))
    op.execute('UPDATE scopus_abstract_defunct SET scopus_id = scopus_id_temp')
    op.create_primary_key('pk_scopus_abstract_defunct', 'scopus_abstract_defunct', ['scopus_id'])
    op.drop_column('scopus_abstract_defunct', 'scopus_id_temp')

    op.add_column('scopus_citation_defunct', sa.Column('scopus_id_temp', sa.String(50), nullable=True))
    op.execute('UPDATE scopus_citation_defunct SET scopus_id_temp = TO_CHAR(scopus_id)')
    op.execute('ALTER TABLE scopus_citation_defunct DROP CONSTRAINT pk_scopus_citation_defunct')
    op.drop_column('scopus_citation_defunct', 'scopus_id')
    op.add_column('scopus_citation_defunct', sa.Column('scopus_id', sa.String(50), nullable=True))
    op.execute('UPDATE scopus_citation_defunct SET scopus_id = scopus_id_temp')
    op.create_primary_key('pk_scopus_citation_defunct', 'scopus_citation_defunct', ['scopus_id'])
    op.drop_column('scopus_citation_defunct', 'scopus_id_temp')

def downgrade():
    op.add_column('scopus_citation_defunct', sa.Column('scopus_id_temp', sa.INTEGER(), nullable=True))
    op.execute('UPDATE scopus_citation_defunct SET scopus_id_temp = TO_NUMBER(scopus_id)')
    op.execute('ALTER TABLE scopus_citation_defunct DROP CONSTRAINT pk_scopus_citation_defunct')
    op.drop_column('scopus_citation_defunct', 'scopus_id')
    op.add_column('scopus_citation_defunct', sa.Column('scopus_id', sa.INTEGER(), nullable=True))
    op.execute('UPDATE scopus_citation_defunct SET scopus_id = scopus_id_temp')
    op.create_primary_key('pk_scopus_citation_defunct', 'scopus_citation_defunct', ['scopus_id'])
    op.drop_column('scopus_citation_defunct', 'scopus_id_temp')

    op.add_column('scopus_abstract_defunct', sa.Column('scopus_id_temp', sa.INTEGER(), nullable=True))
    op.execute('UPDATE scopus_abstract_defunct SET scopus_id_temp = TO_NUMBER(scopus_id)')
    op.execute('ALTER TABLE scopus_abstract_defunct DROP CONSTRAINT pk_scopus_abstract_defunct')
    op.drop_column('scopus_abstract_defunct', 'scopus_id')
    op.add_column('scopus_abstract_defunct', sa.Column('scopus_id', sa.INTEGER(), nullable=True))
    op.execute('UPDATE scopus_abstract_defunct SET scopus_id = scopus_id_temp')
    op.create_primary_key('pk_scopus_abstract_defunct', 'scopus_abstract_defunct', ['scopus_id'])
    op.drop_column('scopus_abstract_defunct', 'scopus_id_temp')
