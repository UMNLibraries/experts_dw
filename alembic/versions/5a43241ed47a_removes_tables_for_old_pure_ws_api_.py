"""Removes tables for old Pure WS (API) versions

Revision ID: 5a43241ed47a
Revises: b4819b11ead7
Create Date: 2026-10-23 09:11:17.663098

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '5a43241ed47a'
down_revision = 'b4819b11ead7'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('pure_json_external_person_523')
    op.drop_table('pure_json_external_person_517_staging')
    op.drop_table('pure_json_research_output_518_staging')
    op.drop_table('pure_json_person_517_staging')
    op.drop_table('pure_json_research_output_517_staging')
    op.drop_table('pure_json_external_person_517')
    op.drop_table('pure_json_person_523')
    op.drop_table('pure_json_organisation_523_staging')
    op.drop_table('pure_json_organisation_523')
    op.drop_table('pure_json_person_517')
    op.drop_table('pure_json_external_organisation_518_staging')
    op.drop_table('pure_json_organisation_517_staging')
    op.drop_table('pure_json_external_organisation_517_staging')
    op.drop_table('pure_json_change_518')
    op.drop_table('pure_json_research_output_523_staging')
    op.drop_table('pure_json_change_523')
    op.drop_table('pure_json_person_518')
    op.drop_table('pure_json_person_518_staging')
    op.drop_table('pure_json_person_523_staging')
    op.drop_table('pure_json_external_person_523_staging')
    op.drop_table('pure_json_external_organisation_523')
    op.drop_table('pure_json_organisation_518')
    op.drop_table('pure_json_external_organisation_517')
    op.drop_table('pure_json_change_517')
    op.drop_table('pure_json_change_517_history')
    op.drop_table('pure_json_external_organisation_523_staging')
    op.drop_table('pure_json_external_person_518_staging')
    op.drop_table('pure_json_organisation_518_staging')
    op.drop_table('pure_json_change_523_history')
    op.drop_table('pure_json_research_output_523')
    op.drop_table('pure_json_research_output_517')
    op.drop_table('pure_json_external_organisation_518')
    op.drop_table('pure_json_change_518_history')
    op.drop_table('pure_json_research_output_518')
    op.drop_table('pure_json_external_person_518')
    op.drop_table('pure_json_organisation_517')


def downgrade():
    op.create_table('pure_json_organisation_517',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_organisation_517_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_organisation_517')
    )
    op.create_table('pure_json_external_person_518',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_external_person_518_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_external_person_518')
    )
    op.create_table('pure_json_research_output_518',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_research_output_518_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_research_output_518')
    )
    op.create_table('pure_json_change_518_history',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('family_system_name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('change_type', sa.VARCHAR(length=10), nullable=False),
    sa.Column('pure_version', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name='pk_pure_json_change_518_history')
    )
    op.create_table('pure_json_external_organisation_518',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_external_organisation_518_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_external_organisation_518')
    )
    op.create_table('pure_json_research_output_517',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_research_output_517_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_research_output_517')
    )
    op.create_table('pure_json_research_output_523',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_research_output_523_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_research_output_523')
    )
    op.create_table('pure_json_change_523_history',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('family_system_name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('change_type', sa.VARCHAR(length=10), nullable=False),
    sa.Column('pure_version', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name='pk_pure_json_change_523_history')
    )
    op.create_table('pure_json_organisation_518_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_organisation_518_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_organisation_518_staging')
    )
    op.create_table('pure_json_external_person_518_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_external_person_518_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_external_person_518_staging')
    )
    op.create_table('pure_json_external_organisation_523_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_external_organisation_523_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name='pk_pure_json_external_organisation_523_staging')
    )
    op.create_table('pure_json_change_517_history',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('family_system_name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('change_type', sa.VARCHAR(length=10), nullable=False),
    sa.Column('pure_version', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name='pk_pure_json_change_517_history')
    )
    op.create_table('pure_json_change_517',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('family_system_name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('change_type', sa.VARCHAR(length=10), nullable=False),
    sa.Column('pure_version', sa.INTEGER(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_change_517_json_document'),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name='pk_pure_json_change_517')
    )
    op.create_table('pure_json_external_organisation_517',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_external_organisation_517_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_external_organisation_517')
    )
    op.create_table('pure_json_organisation_518',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_organisation_518_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_organisation_518')
    )
    op.create_table('pure_json_external_organisation_523',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_external_organisation_523_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_external_organisation_523')
    )
    op.create_table('pure_json_external_person_523_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_external_person_523_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name='pk_pure_json_external_person_523_staging')
    )
    op.create_table('pure_json_person_523_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_person_523_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name='pk_pure_json_person_523_staging')
    )
    op.create_table('pure_json_person_518_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_person_518_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_person_518_staging')
    )
    op.create_table('pure_json_person_518',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_person_518_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_person_518')
    )
    op.create_table('pure_json_change_523',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('family_system_name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('change_type', sa.VARCHAR(length=10), nullable=False),
    sa.Column('pure_version', sa.INTEGER(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_change_523_json_document'),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name='pk_pure_json_change_523')
    )
    op.create_table('pure_json_research_output_523_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_research_output_523_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name='pk_pure_json_research_output_523_staging')
    )
    op.create_table('pure_json_change_518',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('family_system_name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('change_type', sa.VARCHAR(length=10), nullable=False),
    sa.Column('pure_version', sa.INTEGER(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_change_518_json_document'),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name='pk_pure_json_change_518')
    )
    op.create_table('pure_json_external_organisation_517_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_external_organisation_517_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_external_organisation_517_staging')
    )
    op.create_table('pure_json_organisation_517_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_organisation_517_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_organisation_517_staging')
    )
    op.create_table('pure_json_external_organisation_518_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_external_organisation_518_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_external_organisation_518_staging')
    )
    op.create_table('pure_json_person_517',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_person_517_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_person_517')
    )
    op.create_table('pure_json_organisation_523',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_organisation_523_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_organisation_523')
    )
    op.create_table('pure_json_organisation_523_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_organisation_523_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name='pk_pure_json_organisation_523_staging')
    )
    op.create_table('pure_json_person_523',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_person_523_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_person_523')
    )
    op.create_table('pure_json_external_person_517',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_external_person_517_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_external_person_517')
    )
    op.create_table('pure_json_research_output_517_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_research_output_517_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_research_output_517_staging')
    )
    op.create_table('pure_json_person_517_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_person_517_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_person_517_staging')
    )
    op.create_table('pure_json_research_output_518_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_research_output_518_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_research_output_518_staging')
    )
    op.create_table('pure_json_external_person_517_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_external_person_517_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_external_person_517_staging')
    )
    op.create_table('pure_json_external_person_523',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_external_person_523_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_external_person_523')
    )
