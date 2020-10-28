"""Replaces JsonSoda.json_document, but now with data type Text (CLOB)

Revision ID: 56ccd58540f5
Revises: 36edb5e3fe32
Create Date: 2020-10-20 09:56:06.762708

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56ccd58540f5'
down_revision = '36edb5e3fe32'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('pure_json_research_output_516', sa.Column('json_document', sa.Text(), nullable=False))
    op.create_check_constraint('json_document', 'pure_json_research_output_516', 'json_document IS JSON')


def downgrade():
    op.drop_constraint('ck_pure_json_research_output_516_json_document', 'pure_json_research_output_516')
    op.drop_column('pure_json_research_output_516', 'json_document')
