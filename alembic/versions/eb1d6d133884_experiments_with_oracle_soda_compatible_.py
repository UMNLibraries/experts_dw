"""Experiments with Oracle-SODA-compatible tables for JSON

Revision ID: eb1d6d133884
Revises: 04d003b7ad71
Create Date: 2020-10-16 11:47:22.026739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb1d6d133884'
down_revision = '04d003b7ad71'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_json_research_output_516',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.LargeBinary(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_research_output_516_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_research_output_516'))
    )


def downgrade():
    op.drop_table('pure_json_research_output_516')
