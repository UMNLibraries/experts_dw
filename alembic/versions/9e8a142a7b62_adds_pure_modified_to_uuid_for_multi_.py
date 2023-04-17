"""Adds pure_modified to uuid for multi-column staging PKs

Revision ID: 9e8a142a7b62
Revises: e41980d62bde
Create Date: 2023-04-17 13:11:27.894593

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '9e8a142a7b62'
down_revision = 'e41980d62bde'
branch_labels = None
depends_on = None


def upgrade():
    # 524
    op.drop_constraint(
        'PK_PURE_JSON_RESEARCH_OUTPUT_524_STAGING',
        'pure_json_research_output_524_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_RESEARCH_OUTPUT_524_STAGING',
        'pure_json_research_output_524_staging',
        ['uuid', 'pure_modified']
    )
    op.drop_constraint(
        'PK_PURE_JSON_PERSON_524_STAGING',
        'pure_json_person_524_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_PERSON_524_STAGING',
        'pure_json_person_524_staging',
        ['uuid', 'pure_modified']
    )
    op.drop_constraint(
        'PK_PURE_JSON_EXTERNAL_PERSON_524_STAGING',
        'pure_json_external_person_524_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_EXTERNAL_PERSON_524_STAGING',
        'pure_json_external_person_524_staging',
        ['uuid', 'pure_modified']
    )
    op.drop_constraint(
        'PK_PURE_JSON_ORGANISATION_524_STAGING',
        'pure_json_organisation_524_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_ORGANISATION_524_STAGING',
        'pure_json_organisation_524_staging',
        ['uuid', 'pure_modified']
    )
    op.drop_constraint(
        'PK_PURE_JSON_EXTERNAL_ORGANISATION_524_STAGING',
        'pure_json_external_organisation_524_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_EXTERNAL_ORGANISATION_524_STAGING',
        'pure_json_external_organisation_524_staging',
        ['uuid', 'pure_modified']
    )
    op.drop_constraint(
        'PK_PURE_JSON_JOURNAL_524_STAGING',
        'pure_json_journal_524_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_JOURNAL_524_STAGING',
        'pure_json_journal_524_staging',
        ['uuid', 'pure_modified']
    )

    # 523
    op.drop_constraint(
        'PK_PURE_JSON_RESEARCH_OUTPUT_523_STAGING',
        'pure_json_research_output_523_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_RESEARCH_OUTPUT_523_STAGING',
        'pure_json_research_output_523_staging',
        ['uuid', 'pure_modified']
    )
    op.drop_constraint(
        'PK_PURE_JSON_PERSON_523_STAGING',
        'pure_json_person_523_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_PERSON_523_STAGING',
        'pure_json_person_523_staging',
        ['uuid', 'pure_modified']
    )
    op.drop_constraint(
        'PK_PURE_JSON_EXTERNAL_PERSON_523_STAGING',
        'pure_json_external_person_523_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_EXTERNAL_PERSON_523_STAGING',
        'pure_json_external_person_523_staging',
        ['uuid', 'pure_modified']
    )
    op.drop_constraint(
        'PK_PURE_JSON_ORGANISATION_523_STAGING',
        'pure_json_organisation_523_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_ORGANISATION_523_STAGING',
        'pure_json_organisation_523_staging',
        ['uuid', 'pure_modified']
    )
    op.drop_constraint(
        'PK_PURE_JSON_EXTERNAL_ORGANISATION_523_STAGING',
        'pure_json_external_organisation_523_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_EXTERNAL_ORGANISATION_523_STAGING',
        'pure_json_external_organisation_523_staging',
        ['uuid', 'pure_modified']
    )

def downgrade():
    # 524
    op.drop_constraint(
        'PK_PURE_JSON_RESEARCH_OUTPUT_524_STAGING',
        'pure_json_research_output_524_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_RESEARCH_OUTPUT_524_STAGING',
        'pure_json_research_output_524_staging',
        ['uuid']
    )
    op.drop_constraint(
        'PK_PURE_JSON_PERSON_524_STAGING',
        'pure_json_person_524_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_PERSON_524_STAGING',
        'pure_json_person_524_staging',
        ['uuid']
    )
    op.drop_constraint(
        'PK_PURE_JSON_EXTERNAL_PERSON_524_STAGING',
        'pure_json_external_person_524_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_EXTERNAL_PERSON_524_STAGING',
        'pure_json_external_person_524_staging',
        ['uuid']
    )
    op.drop_constraint(
        'PK_PURE_JSON_ORGANISATION_524_STAGING',
        'pure_json_organisation_524_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_ORGANISATION_524_STAGING',
        'pure_json_organisation_524_staging',
        ['uuid']
    )
    op.drop_constraint(
        'PK_PURE_JSON_EXTERNAL_ORGANISATION_524_STAGING',
        'pure_json_external_organisation_524_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_EXTERNAL_ORGANISATION_524_STAGING',
        'pure_json_external_organisation_524_staging',
        ['uuid']
    )
    op.drop_constraint(
        'PK_PURE_JSON_JOURNAL_524_STAGING',
        'pure_json_journal_524_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_JOURNAL_524_STAGING',
        'pure_json_journal_524_staging',
        ['uuid']
    )

    # 523
    op.drop_constraint(
        'PK_PURE_JSON_RESEARCH_OUTPUT_523_STAGING',
        'pure_json_research_output_523_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_RESEARCH_OUTPUT_523_STAGING',
        'pure_json_research_output_523_staging',
        ['uuid']
    )
    op.drop_constraint(
        'PK_PURE_JSON_PERSON_523_STAGING',
        'pure_json_person_523_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_PERSON_523_STAGING',
        'pure_json_person_523_staging',
        ['uuid']
    )
    op.drop_constraint(
        'PK_PURE_JSON_EXTERNAL_PERSON_523_STAGING',
        'pure_json_external_person_523_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_EXTERNAL_PERSON_523_STAGING',
        'pure_json_external_person_523_staging',
        ['uuid']
    )
    op.drop_constraint(
        'PK_PURE_JSON_ORGANISATION_523_STAGING',
        'pure_json_organisation_523_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_ORGANISATION_523_STAGING',
        'pure_json_organisation_523_staging',
        ['uuid']
    )
    op.drop_constraint(
        'PK_PURE_JSON_EXTERNAL_ORGANISATION_523_STAGING',
        'pure_json_external_organisation_523_staging',
        type_='primary'
    )
    op.create_primary_key(
        'PK_PURE_JSON_EXTERNAL_ORGANISATION_523_STAGING',
        'pure_json_external_organisation_523_staging',
        ['uuid']
    )
