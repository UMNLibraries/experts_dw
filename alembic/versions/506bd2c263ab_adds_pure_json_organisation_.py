"""Adds pure_json_organisation* tables.

Revision ID: 506bd2c263ab
Revises: edeb7133b093
Create Date: 2020-11-11 11:54:00.353319

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '506bd2c263ab'
down_revision = 'edeb7133b093'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_json_organisation_516',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_organisation_516_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_organisation_516'))
    )
    op.create_table('pure_json_organisation_516_staging',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_organisation_516_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_organisation_516_staging'))
    )


def downgrade():
    op.drop_constraint(
        'ck_pure_json_organisation_516_staging_json_document',
        'pure_json_organisation_516_staging'
    )
    op.drop_table('pure_json_organisation_516_staging')
    op.drop_constraint(
        'ck_pure_json_organisation_516_json_document',
        'pure_json_organisation_516'
    )
    op.drop_table('pure_json_organisation_516')
