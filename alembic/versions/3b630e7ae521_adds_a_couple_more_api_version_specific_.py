"""Adds a couple more api-version-specific JSON staging and change tables

Revision ID: 3b630e7ae521
Revises: 0001b1376305
Create Date: 2020-10-22 14:45:07.652503

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3b630e7ae521'
down_revision = '0001b1376305'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_json_change_516',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('pure_version', sa.Integer(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_change_516_json_document')),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name=op.f('pk_pure_json_change_516'))
    )
    op.create_table('pure_json_change_516_history',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('pure_version', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name=op.f('pk_pure_json_change_516_history'))
    )
    op.create_table('pure_json_research_output_516_staging',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_research_output_516_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_research_output_516_staging'))
    )


def downgrade():
    op.drop_table('pure_json_research_output_516_staging')
    op.drop_table('pure_json_change_516_history')
    op.drop_table('pure_json_change_516')
