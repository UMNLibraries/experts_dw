"""Adds pure_json*518 tables.

Revision ID: 3a57965067e9
Revises: 77100ddf3163
Create Date: 2021-06-09 10:53:13.958035

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '3a57965067e9'
down_revision = '77100ddf3163'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_json_change_518',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('pure_version', sa.Integer(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_change_518_json_document')),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name=op.f('pk_pure_json_change_518'))
    )
    op.create_table('pure_json_change_518_history',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('pure_version', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name=op.f('pk_pure_json_change_518_history'))
    )
    op.create_table('pure_json_external_organisation_518',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_external_organisation_518_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_external_organisation_518'))
    )
    op.create_table('pure_json_external_organisation_518_staging',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_external_organisation_518_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_external_organisation_518_staging'))
    )
    op.create_table('pure_json_external_person_518',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_external_person_518_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_external_person_518'))
    )
    op.create_table('pure_json_external_person_518_staging',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_external_person_518_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_external_person_518_staging'))
    )
    op.create_table('pure_json_organisation_518',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_organisation_518_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_organisation_518'))
    )
    op.create_table('pure_json_organisation_518_staging',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_organisation_518_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_organisation_518_staging'))
    )
    op.create_table('pure_json_person_518',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_person_518_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_person_518'))
    )
    op.create_table('pure_json_person_518_staging',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_person_518_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_person_518_staging'))
    )
    op.create_table('pure_json_research_output_518',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_research_output_518_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_research_output_518'))
    )
    op.create_table('pure_json_research_output_518_staging',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_research_output_518_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_research_output_518_staging'))
    )

def downgrade():
    op.drop_table('pure_json_research_output_518_staging')
    op.drop_table('pure_json_research_output_518')
    op.drop_table('pure_json_person_518_staging')
    op.drop_table('pure_json_person_518')
    op.drop_table('pure_json_organisation_518_staging')
    op.drop_table('pure_json_organisation_518')
    op.drop_table('pure_json_external_person_518_staging')
    op.drop_table('pure_json_external_person_518')
    op.drop_table('pure_json_external_organisation_518_staging')
    op.drop_table('pure_json_external_organisation_518')
    op.drop_table('pure_json_change_518_history')
    op.drop_table('pure_json_change_518')
