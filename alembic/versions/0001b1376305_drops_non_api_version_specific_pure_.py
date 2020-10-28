"""Drops non-api-version-specific pure_json* tables

Revision ID: 0001b1376305
Revises: 56ccd58540f5
Create Date: 2020-10-22 13:30:13.615688

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '0001b1376305'
down_revision = '56ccd58540f5'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('pure_json_research_output_previous_uuid')
    op.drop_table('pure_json_change_history')
    op.drop_constraint('ck_pure_json_person_record', 'pure_json_person')
    op.drop_table('pure_json_person')
    op.drop_constraint('ck_pure_json_person_staging_record', 'pure_json_person_staging')
    op.drop_table('pure_json_person_staging')
    op.drop_constraint('ck_pure_json_change_record', 'pure_json_change')
    op.drop_table('pure_json_change')
    op.drop_constraint('ck_pure_json_research_output_record', 'pure_json_research_output')
    op.drop_table('pure_json_research_output')
    op.drop_constraint('ck_pure_json_research_output_staging_record', 'pure_json_research_output_staging')
    op.drop_table('pure_json_research_output_staging')


def downgrade():
    op.create_table('pure_json_person_staging',
    sa.Column('record', sa.CLOB(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('api_version', sa.VARCHAR(length=10), nullable=False),
    sa.Column('modified', oracle.DATE(), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.CheckConstraint('record IS JSON', name='ck_pure_json_person_staging_record'),
    sa.PrimaryKeyConstraint('uuid', 'api_version', name='pk_pure_json_person_staging')
    )
    op.create_table('pure_json_research_output_staging',
    sa.Column('record', sa.CLOB(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('api_version', sa.VARCHAR(length=10), nullable=False),
    sa.Column('modified', oracle.DATE(), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.CheckConstraint('record IS JSON', name='ck_pure_json_research_output_staging_record'),
    sa.PrimaryKeyConstraint('uuid', 'api_version', name='pk_pure_json_research_output_staging')
    )
    op.create_table('pure_json_research_output',
    sa.Column('record', sa.CLOB(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('api_version', sa.VARCHAR(length=10), nullable=False),
    sa.Column('modified', oracle.DATE(), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.CheckConstraint('record IS JSON', name='ck_pure_json_research_output_record'),
    sa.PrimaryKeyConstraint('uuid', 'api_version', name='pk_pure_json_research_output')
    )
    op.create_table('pure_json_change',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('api_version', sa.VARCHAR(length=10), nullable=False),
    sa.Column('family_system_name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('change_type', sa.VARCHAR(length=10), nullable=False),
    sa.Column('version', sa.INTEGER(), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('record', sa.CLOB(), nullable=False),
    sa.CheckConstraint('record IS JSON', name='ck_pure_json_change_record'),
    sa.PrimaryKeyConstraint('uuid', 'api_version', 'version', name='pk_pure_json_change')
    )
    op.create_table('pure_json_person',
    sa.Column('record', sa.CLOB(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('api_version', sa.VARCHAR(length=10), nullable=False),
    sa.Column('modified', oracle.DATE(), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.CheckConstraint('record IS JSON', name='ck_pure_json_person_record'),
    sa.PrimaryKeyConstraint('uuid', 'api_version', name='pk_pure_json_person')
    )
    op.create_table('pure_json_change_history',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('api_version', sa.VARCHAR(length=10), nullable=False),
    sa.Column('family_system_name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('change_type', sa.VARCHAR(length=10), nullable=False),
    sa.Column('version', sa.INTEGER(), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('processed', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'api_version', 'version', name='pk_pure_json_change_history')
    )
    op.create_table('pure_json_research_output_previous_uuid',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('previous_uuid', sa.VARCHAR(length=36), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'previous_uuid', name='pk_pure_json_research_output_previous_uuid')
    )
