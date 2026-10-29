"""Adds pure_json* tables that use BLOBs for json_documents

Revision ID: 01df18fff375
Revises: 9c89f2824567
Create Date: 2026-10-27 07:14:45.017892

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '01df18fff375'
down_revision = '9c89f2824567'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_json_change_524',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.BLOB(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('pure_version', sa.Integer(), nullable=False),
    sa.CheckConstraint('json_document IS JSON FORMAT OSON', name=op.f('ck_pure_json_change_524_json_document')),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name=op.f('pk_pure_json_change_524'))
    )
    op.create_table('pure_json_change_524_history',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('pure_version', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name=op.f('pk_pure_json_change_524_history'))
    )
    op.create_table('pure_json_external_organisation_524',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.BLOB(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON FORMAT OSON', name=op.f('ck_pure_json_external_organisation_524_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_external_organisation_524'))
    )
    op.create_table('pure_json_external_organisation_524_staging',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.BLOB(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON FORMAT OSON', name=op.f('ck_pure_json_external_organisation_524_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name=op.f('pk_pure_json_external_organisation_524_staging'))
    )
    op.create_table('pure_json_external_person_524',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.BLOB(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON FORMAT OSON', name=op.f('ck_pure_json_external_person_524_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_external_person_524'))
    )
    op.create_table('pure_json_external_person_524_staging',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.BLOB(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON FORMAT OSON', name=op.f('ck_pure_json_external_person_524_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name=op.f('pk_pure_json_external_person_524_staging'))
    )
    op.create_table('pure_json_journal_524',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.BLOB(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON FORMAT OSON', name=op.f('ck_pure_json_journal_524_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_journal_524'))
    )
    op.create_table('pure_json_journal_524_staging',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.BLOB(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON FORMAT OSON', name=op.f('ck_pure_json_journal_524_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name=op.f('pk_pure_json_journal_524_staging'))
    )
    op.create_table('pure_json_organisation_524',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.BLOB(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON FORMAT OSON', name=op.f('ck_pure_json_organisation_524_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_organisation_524'))
    )
    op.create_table('pure_json_organisation_524_staging',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.BLOB(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON FORMAT OSON', name=op.f('ck_pure_json_organisation_524_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name=op.f('pk_pure_json_organisation_524_staging'))
    )
    op.create_table('pure_json_person_524',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.BLOB(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON FORMAT OSON', name=op.f('ck_pure_json_person_524_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_person_524'))
    )
    op.create_table('pure_json_person_524_staging',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.BLOB(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON FORMAT OSON', name=op.f('ck_pure_json_person_524_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name=op.f('pk_pure_json_person_524_staging'))
    )
    op.create_table('pure_json_research_output_524',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.BLOB(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON FORMAT OSON', name=op.f('ck_pure_json_research_output_524_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_research_output_524'))
    )
    op.create_table('pure_json_research_output_524_staging',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.BLOB(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON FORMAT OSON', name=op.f('ck_pure_json_research_output_524_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', 'pure_modified', name=op.f('pk_pure_json_research_output_524_staging'))
    )

def downgrade():
    op.drop_table('pure_json_research_output_524_staging')
    op.drop_table('pure_json_research_output_524')
    op.drop_table('pure_json_person_524_staging')
    op.drop_table('pure_json_person_524')
    op.drop_table('pure_json_organisation_524_staging')
    op.drop_table('pure_json_organisation_524')
    op.drop_table('pure_json_journal_524_staging')
    op.drop_table('pure_json_journal_524')
    op.drop_table('pure_json_external_person_524_staging')
    op.drop_table('pure_json_external_person_524')
    op.drop_table('pure_json_external_organisation_524_staging')
    op.drop_table('pure_json_external_organisation_524')
    op.drop_table('pure_json_change_524_history')
    op.drop_table('pure_json_change_524')
