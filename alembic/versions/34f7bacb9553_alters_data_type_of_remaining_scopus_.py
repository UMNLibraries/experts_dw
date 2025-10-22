"""Alters data type of remaining scopus_json*.scopus_id columns

Revision ID: 34f7bacb9553
Revises: a273274dc2cf
Create Date: 2025-10-22 10:35:39.446827

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '34f7bacb9553'
down_revision = 'a273274dc2cf'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('scopus_json_abstract_staging', sa.Column('scopus_id_temp', sa.String(50), nullable=True))
    op.execute('UPDATE scopus_json_abstract_staging SET scopus_id_temp = TO_CHAR(scopus_id)')
    op.execute('ALTER TABLE scopus_json_abstract_staging DROP CONSTRAINT pk_scopus_json_abstract_staging')
    op.drop_column('scopus_json_abstract_staging', 'scopus_id')
    op.add_column('scopus_json_abstract_staging', sa.Column('scopus_id', sa.String(50), nullable=True))
    op.execute('UPDATE scopus_json_abstract_staging SET scopus_id = scopus_id_temp')
    op.create_primary_key('pk_scopus_json_abstract_staging', 'scopus_json_abstract_staging', ['scopus_id','scopus_modified'])
    op.drop_column('scopus_json_abstract_staging', 'scopus_id_temp')

    op.add_column('scopus_json_citation', sa.Column('scopus_id_temp', sa.String(50), nullable=True))
    op.execute('UPDATE scopus_json_citation SET scopus_id_temp = TO_CHAR(scopus_id)')
    op.execute('ALTER TABLE scopus_json_citation DROP CONSTRAINT pk_scopus_json_citation')
    op.drop_column('scopus_json_citation', 'scopus_id')
    op.add_column('scopus_json_citation', sa.Column('scopus_id', sa.String(50), nullable=True))
    op.execute('UPDATE scopus_json_citation SET scopus_id = scopus_id_temp')
    op.create_primary_key('pk_scopus_json_citation', 'scopus_json_citation', ['scopus_id'])
    op.drop_column('scopus_json_citation', 'scopus_id_temp')

    op.add_column('scopus_json_citation_staging', sa.Column('scopus_id_temp', sa.String(50), nullable=True))
    op.execute('UPDATE scopus_json_citation_staging SET scopus_id_temp = TO_CHAR(scopus_id)')
    op.execute('ALTER TABLE scopus_json_citation_staging DROP CONSTRAINT pk_scopus_json_citation_staging')
    op.drop_column('scopus_json_citation_staging', 'scopus_id')
    op.add_column('scopus_json_citation_staging', sa.Column('scopus_id', sa.String(50), nullable=True))
    op.execute('UPDATE scopus_json_citation_staging SET scopus_id = scopus_id_temp')
    op.create_primary_key('pk_scopus_json_citation_staging', 'scopus_json_citation_staging', ['scopus_id','scopus_modified'])
    op.drop_column('scopus_json_citation_staging', 'scopus_id_temp')

def downgrade():
    op.add_column('scopus_json_citation_staging', sa.Column('scopus_id_temp', sa.INTEGER(), nullable=True))
    op.execute('UPDATE scopus_json_citation_staging SET scopus_id_temp = TO_NUMBER(scopus_id)')
    op.execute('ALTER TABLE scopus_json_citation_staging DROP CONSTRAINT pk_scopus_json_citation_staging')
    op.drop_column('scopus_json_citation_staging', 'scopus_id')
    op.add_column('scopus_json_citation_staging', sa.Column('scopus_id', sa.INTEGER(), nullable=True))
    op.execute('UPDATE scopus_json_citation_staging SET scopus_id = scopus_id_temp')
    op.create_primary_key('pk_scopus_json_citation_staging', 'scopus_json_citation_staging', ['scopus_id','scopus_modified'])
    op.drop_column('scopus_json_citation_staging', 'scopus_id_temp')

    op.add_column('scopus_json_citation', sa.Column('scopus_id_temp', sa.INTEGER(), nullable=True))
    op.execute('UPDATE scopus_json_citation SET scopus_id_temp = TO_NUMBER(scopus_id)')
    op.execute('ALTER TABLE scopus_json_citation DROP CONSTRAINT pk_scopus_json_citation')
    op.drop_column('scopus_json_citation', 'scopus_id')
    op.add_column('scopus_json_citation', sa.Column('scopus_id', sa.INTEGER(), nullable=True))
    op.execute('UPDATE scopus_json_citation SET scopus_id = scopus_id_temp')
    op.create_primary_key('pk_scopus_json_citation', 'scopus_json_citation', ['scopus_id'])
    op.drop_column('scopus_json_citation', 'scopus_id_temp')

    op.add_column('scopus_json_abstract_staging', sa.Column('scopus_id_temp', sa.INTEGER(), nullable=True))
    op.execute('UPDATE scopus_json_abstract_staging SET scopus_id_temp = TO_NUMBER(scopus_id)')
    op.execute('ALTER TABLE scopus_json_abstract_staging DROP CONSTRAINT pk_scopus_json_abstract_staging')
    op.drop_column('scopus_json_abstract_staging', 'scopus_id')
    op.add_column('scopus_json_abstract_staging', sa.Column('scopus_id', sa.INTEGER(), nullable=True))
    op.execute('UPDATE scopus_json_abstract_staging SET scopus_id = scopus_id_temp')
    op.create_primary_key('pk_scopus_json_abstract_staging', 'scopus_json_abstract_staging', ['scopus_id','scopus_modified'])
    op.drop_column('scopus_json_abstract_staging', 'scopus_id_temp')
