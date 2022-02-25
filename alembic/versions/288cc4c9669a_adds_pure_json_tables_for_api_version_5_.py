"""Adds Pure JSON tables for API version 5.23.

Revision ID: 288cc4c9669a
Revises: c4751a4dbc56
Create Date: 2022-02-25 12:53:02.034282

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '288cc4c9669a'
down_revision = 'c4751a4dbc56'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_json_change_523',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('pure_version', sa.Integer(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_change_523_json_document')),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name=op.f('pk_pure_json_change_523'))
    )
    op.create_table('pure_json_change_523_history',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('pure_version', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name=op.f('pk_pure_json_change_523_history'))
    )
    op.create_table('pure_json_external_organisation_523',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_external_organisation_523_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_external_organisation_523'))
    )
    op.create_table('pure_json_external_organisation_523_staging',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_external_organisation_523_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_external_organisation_523_staging'))
    )
    op.create_table('pure_json_external_person_523',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_external_person_523_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_external_person_523'))
    )
    op.create_table('pure_json_external_person_523_staging',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_external_person_523_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_external_person_523_staging'))
    )
    op.create_table('pure_json_organisation_523',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_organisation_523_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_organisation_523'))
    )
    op.create_table('pure_json_organisation_523_staging',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_organisation_523_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_organisation_523_staging'))
    )
    op.create_table('pure_json_person_523',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_person_523_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_person_523'))
    )
    op.create_table('pure_json_person_523_staging',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_person_523_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_person_523_staging'))
    )
    op.create_table('pure_json_research_output_523',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_research_output_523_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_research_output_523'))
    )
    op.create_table('pure_json_research_output_523_staging',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_research_output_523_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_research_output_523_staging'))
    )


def downgrade():
    op.drop_table('pure_json_research_output_523_staging')
    op.drop_table('pure_json_research_output_523')
    op.drop_table('pure_json_person_523_staging')
    op.drop_table('pure_json_person_523')
    op.drop_table('pure_json_organisation_523_staging')
    op.drop_table('pure_json_organisation_523')
    op.drop_table('pure_json_external_person_523_staging')
    op.drop_table('pure_json_external_person_523')
    op.drop_table('pure_json_external_organisation_523_staging')
    op.drop_table('pure_json_external_organisation_523')
    op.drop_table('pure_json_change_523_history')
    op.drop_table('pure_json_change_523')
