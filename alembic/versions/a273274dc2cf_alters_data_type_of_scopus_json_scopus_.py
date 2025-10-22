"""Alters data type of scopus_json*.scopus_id columns

Revision ID: a273274dc2cf
Revises: a939db178cec
Create Date: 2025-10-21 14:26:25.441274

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'a273274dc2cf'
down_revision = 'a939db178cec'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('scopus_json_abstract', sa.Column('scopus_id_temp', sa.String(50), nullable=True))
    op.execute('UPDATE scopus_json_abstract SET scopus_id_temp = TO_CHAR(scopus_id)')
    op.execute('ALTER TABLE scopus_json_abstract DROP CONSTRAINT pk_scopus_json_abstract')
    op.drop_column('scopus_json_abstract', 'scopus_id')
    op.add_column('scopus_json_abstract', sa.Column('scopus_id', sa.String(50), nullable=True))
    op.execute('UPDATE scopus_json_abstract SET scopus_id = scopus_id_temp')
    op.create_primary_key('pk_scopus_json_abstract', 'scopus_json_abstract', ['scopus_id'])
    op.drop_column('scopus_json_abstract', 'scopus_id_temp')

def downgrade():
    op.add_column('scopus_json_abstract', sa.Column('scopus_id_temp', sa.INTEGER(), nullable=True))
    op.execute('UPDATE scopus_json_abstract SET scopus_id_temp = TO_NUMBER(scopus_id)')
    op.execute('ALTER TABLE scopus_json_abstract DROP CONSTRAINT pk_scopus_json_abstract')
    op.drop_column('scopus_json_abstract', 'scopus_id')
    op.add_column('scopus_json_abstract', sa.Column('scopus_id', sa.INTEGER(), nullable=True))
    op.execute('UPDATE scopus_json_abstract SET scopus_id = scopus_id_temp')
    op.create_primary_key('pk_scopus_json_abstract', 'scopus_json_abstract', ['scopus_id'])
    op.drop_column('scopus_json_abstract', 'scopus_id_temp')
