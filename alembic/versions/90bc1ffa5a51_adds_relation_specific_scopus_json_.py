"""Adds relation-specific Scopus JSON tables

Revision ID: 90bc1ffa5a51
Revises: 01f5d5168215
Create Date: 2024-07-24 16:04:00.527596

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '90bc1ffa5a51'
down_revision = '01f5d5168215'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('scopus_json_abstract_authored',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('scopus_id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('scopus_created', sa.DateTime(), nullable=False),
    sa.Column('scopus_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_scopus_json_abstract_authored_json_document')),
    sa.PrimaryKeyConstraint('scopus_id', name=op.f('pk_scopus_json_abstract_authored'))
    )
    op.create_table('scopus_json_abstract_authored_staging',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('scopus_id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('scopus_created', sa.DateTime(), nullable=False),
    sa.Column('scopus_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_scopus_json_abstract_authored_staging_json_document')),
    sa.PrimaryKeyConstraint('scopus_id', 'scopus_modified', name=op.f('pk_scopus_json_abstract_authored_staging'))
    )
    op.create_table('scopus_json_abstract_cited',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('scopus_id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('scopus_created', sa.DateTime(), nullable=False),
    sa.Column('scopus_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_scopus_json_abstract_cited_json_document')),
    sa.PrimaryKeyConstraint('scopus_id', name=op.f('pk_scopus_json_abstract_cited'))
    )
    op.create_table('scopus_json_abstract_cited_staging',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('scopus_id', sa.Integer(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('scopus_created', sa.DateTime(), nullable=False),
    sa.Column('scopus_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_scopus_json_abstract_cited_staging_json_document')),
    sa.PrimaryKeyConstraint('scopus_id', 'scopus_modified', name=op.f('pk_scopus_json_abstract_cited_staging'))
    )

def downgrade():
    op.drop_table('scopus_json_abstract_cited_staging')
    op.drop_table('scopus_json_abstract_cited')
    op.drop_table('scopus_json_abstract_authored_staging')
    op.drop_table('scopus_json_abstract_authored')
