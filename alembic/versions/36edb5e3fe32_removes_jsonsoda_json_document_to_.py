"""Removes JsonSoda.json_document to prepare for replacement and data type conversion

Revision ID: 36edb5e3fe32
Revises: eb1d6d133884
Create Date: 2020-10-20 09:49:23.186492

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36edb5e3fe32'
down_revision = 'eb1d6d133884'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('ck_pure_json_research_output_516_json_document', 'pure_json_research_output_516')
    op.drop_column('pure_json_research_output_516', 'json_document')


def downgrade():
    op.add_column('pure_json_research_output_516', sa.Column('json_document', sa.BLOB(), nullable=False))
    op.create_check_constraint('json_document', 'pure_json_research_output_516', 'json_document IS JSON')
