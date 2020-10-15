"""Removes 516 version from pure_json table names, adds api_version column, renames downloaded to inserted.

Revision ID: 3066f3c72ecf
Revises: f77be308a99e
Create Date: 2020-09-28 18:09:16.475834

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '3066f3c72ecf'
down_revision = 'f77be308a99e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_json_change',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('api_version', sa.String(length=10), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('record', sa.Text(), nullable=False),
    sa.CheckConstraint('record IS JSON', name=op.f('ck_pure_json_change_record')),
    sa.PrimaryKeyConstraint('uuid', 'api_version', 'version', name=op.f('pk_pure_json_change'))
    )
    op.create_table('pure_json_change_history',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('api_version', sa.String(length=10), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('processed', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'api_version', 'version', name=op.f('pk_pure_json_change_history'))
    )
    op.create_table('pure_json_person',
    sa.Column('record', sa.Text(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('api_version', sa.String(length=10), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.CheckConstraint('record IS JSON', name=op.f('ck_pure_json_person_record')),
    sa.PrimaryKeyConstraint('uuid', 'api_version', name=op.f('pk_pure_json_person'))
    )
    op.create_table('pure_json_person_staging',
    sa.Column('record', sa.Text(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('api_version', sa.String(length=10), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.CheckConstraint('record IS JSON', name=op.f('ck_pure_json_person_staging_record')),
    sa.PrimaryKeyConstraint('uuid', 'api_version', name=op.f('pk_pure_json_person_staging'))
    )
    op.create_table('pure_json_research_output',
    sa.Column('record', sa.Text(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('api_version', sa.String(length=10), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.CheckConstraint('record IS JSON', name=op.f('ck_pure_json_research_output_record')),
    sa.PrimaryKeyConstraint('uuid', 'api_version', name=op.f('pk_pure_json_research_output'))
    )
    op.create_table('pure_json_research_output_staging',
    sa.Column('record', sa.Text(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('api_version', sa.String(length=10), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.CheckConstraint('record IS JSON', name=op.f('ck_pure_json_research_output_staging_record')),
    sa.PrimaryKeyConstraint('uuid', 'api_version', name=op.f('pk_pure_json_research_output_staging'))
    )
    op.drop_table('pure_json_change_516')
    op.drop_table('pure_json_change_516_history')
    op.drop_table('pure_json_person_516')
    op.drop_table('pure_json_person_516_staging')
    op.drop_table('pure_json_research_output_516')
    op.drop_table('pure_json_research_output_516_staging')

def downgrade():
    op.create_table('pure_json_change_516',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('family_system_name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('change_type', sa.VARCHAR(length=10), nullable=False),
    sa.Column('version', sa.INTEGER(), nullable=False),
    sa.Column('downloaded', oracle.DATE(), nullable=False),
    sa.Column('record', sa.CLOB(), nullable=False),
    sa.CheckConstraint('record IS JSON', name='ck_pure_json_change_516_record_json'),
    sa.PrimaryKeyConstraint('uuid', 'version', name='pk_pure_json_change_516')
    )
    op.create_table('pure_json_change_516_history',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('family_system_name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('change_type', sa.VARCHAR(length=10), nullable=False),
    sa.Column('version', sa.INTEGER(), nullable=False),
    sa.Column('downloaded', oracle.DATE(), nullable=False),
    sa.Column('processed', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'version', name='pk_pure_json_change_516_history')
    )
    op.create_table('pure_json_person_516',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('modified', oracle.DATE(), nullable=False),
    sa.Column('downloaded', oracle.DATE(), nullable=True),
    sa.Column('record', sa.CLOB(), nullable=False),
    sa.CheckConstraint('record IS JSON', name='ck_pure_json_person_516_record_json'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_person_516')
    )
    op.create_table('pure_json_person_516_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('modified', oracle.DATE(), nullable=False),
    sa.Column('downloaded', oracle.DATE(), nullable=True),
    sa.Column('record', sa.CLOB(), nullable=False),
    sa.CheckConstraint('record IS JSON', name='ck_pure_json_person_516_staging_record_json'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_person_516_staging')
    )
    op.create_table('pure_json_research_output_516',
    sa.Column('record', sa.CLOB(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('modified', oracle.DATE(), nullable=False),
    sa.Column('downloaded', oracle.DATE(), nullable=True),
    sa.CheckConstraint('record IS JSON', name='ck_pure_json_research_output_516_record'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_research_output_516')
    )
    op.create_table('pure_json_research_output_516_staging',
    sa.Column('record', sa.CLOB(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('modified', oracle.DATE(), nullable=False),
    sa.Column('downloaded', oracle.DATE(), nullable=True),
    sa.CheckConstraint('record IS JSON', name='ck_pure_json_research_output_516_staging_record'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_research_output_516_staging')
    )
    op.drop_table('pure_json_change')
    op.drop_table('pure_json_change_history')
    op.drop_table('pure_json_person')
    op.drop_table('pure_json_person_staging')
    op.drop_table('pure_json_research_output')
    op.drop_table('pure_json_research_output_staging')
