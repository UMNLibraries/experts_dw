"""Removes pure_json* tables that use CLOBs for json_documents

Revision ID: 9c89f2824567
Revises: 5a43241ed47a
Create Date: 2026-10-26 18:30:59.872167

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '9c89f2824567'
down_revision = '5a43241ed47a'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('pure_json_change_524')
    op.drop_table('pure_json_change_524_history')
    op.drop_table('pure_json_external_organisation_524')
    op.drop_table('pure_json_external_organisation_524_staging')
    op.drop_table('pure_json_external_person_524')
    op.drop_table('pure_json_external_person_524_staging')
    op.drop_table('pure_json_journal_524')
    op.drop_table('pure_json_journal_524_staging')
    op.drop_table('pure_json_organisation_524')
    op.drop_table('pure_json_organisation_524_staging')
    op.drop_table('pure_json_person_524')
    op.drop_table('pure_json_person_524_staging')
    op.drop_table('pure_json_research_output_524')
    op.drop_table('pure_json_research_output_524_staging')


def downgrade():
    op.create_table('pure_json_change_524',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('family_system_name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('change_type', sa.VARCHAR(length=10), nullable=False),
    sa.Column('pure_version', sa.INTEGER(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_change_524_json_document'),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name='pk_pure_json_change_524')
    )
    op.create_table('pure_json_change_524_history',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('family_system_name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('change_type', sa.VARCHAR(length=10), nullable=False),
    sa.Column('pure_version', sa.INTEGER(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name='pk_pure_json_change_524_history')
    )
    op.create_table('pure_json_external_organisation_524',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_external_organisation_524_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_external_organisation_524')
    )
    op.create_table('pure_json_external_organisation_524_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_external_organisation_524_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name='pk_pure_json_external_organisation_524_staging')
    )
    op.create_table('pure_json_external_person_524',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_external_person_524_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_external_person_524')
    )
    op.create_table('pure_json_external_person_524_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_external_person_524_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name='pk_pure_json_external_person_524_staging')
    )
    op.create_table('pure_json_journal_524',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_journal_524_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_journal_524')
    )
    op.create_table('pure_json_journal_524_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_journal_524_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name='pk_pure_json_journal_524_staging')
    )
    op.create_table('pure_json_organisation_524',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_organisation_524_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_organisation_524')
    )
    op.create_table('pure_json_organisation_524_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_organisation_524_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name='pk_pure_json_organisation_524_staging')
    )
    op.create_table('pure_json_person_524',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_person_524_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_person_524')
    )
    op.create_table('pure_json_person_524_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_person_524_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name='pk_pure_json_person_524_staging')
    )
    op.create_table('pure_json_research_output_524',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_research_output_524_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_research_output_524')
    )
    op.create_table('pure_json_research_output_524_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_research_output_524_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name='pk_pure_json_research_output_524_staging')
    )
