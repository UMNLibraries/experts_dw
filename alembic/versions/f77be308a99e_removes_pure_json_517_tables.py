"""Removes pure_json*517 tables.

Revision ID: f77be308a99e
Revises: dd6b30729a5b
Create Date: 2020-09-28 17:59:39.981170

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'f77be308a99e'
down_revision = 'dd6b30729a5b'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('pure_json_change_517')
    op.drop_table('pure_json_change_517_history')
    op.drop_table('pure_json_person_517')
    op.drop_table('pure_json_person_517_staging')
    op.drop_table('pure_json_research_output_517')
    op.drop_table('pure_json_research_output_517_staging')


def downgrade():
    op.create_table('pure_json_change_517',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('family_system_name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('change_type', sa.VARCHAR(length=10), nullable=False),
    sa.Column('version', sa.INTEGER(), nullable=False),
    sa.Column('downloaded', oracle.DATE(), nullable=False),
    sa.Column('record', sa.CLOB(), nullable=False),
    sa.CheckConstraint('record IS JSON', name='ck_pure_json_change_517_record_json'),
    sa.PrimaryKeyConstraint('uuid', 'version', name='pk_pure_json_change_517')
    )
    op.create_table('pure_json_change_517_history',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('family_system_name', sa.VARCHAR(length=150), nullable=False),
    sa.Column('change_type', sa.VARCHAR(length=10), nullable=False),
    sa.Column('version', sa.INTEGER(), nullable=False),
    sa.Column('downloaded', oracle.DATE(), nullable=False),
    sa.Column('processed', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'version', name='pk_pure_json_change_517_history')
    )
    op.create_table('pure_json_person_517',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('modified', oracle.DATE(), nullable=False),
    sa.Column('downloaded', oracle.DATE(), nullable=True),
    sa.Column('record', sa.CLOB(), nullable=False),
    sa.CheckConstraint('record IS JSON', name='ck_pure_json_person_517_record_json'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_person_517')
    )
    op.create_table('pure_json_person_517_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('modified', oracle.DATE(), nullable=False),
    sa.Column('downloaded', oracle.DATE(), nullable=True),
    sa.Column('record', sa.CLOB(), nullable=False),
    sa.CheckConstraint('record IS JSON', name='ck_pure_json_person_517_staging_record_json'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_person_517_staging')
    )
    op.create_table('pure_json_research_output_517',
    sa.Column('record', sa.CLOB(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('modified', oracle.DATE(), nullable=False),
    sa.Column('downloaded', oracle.DATE(), nullable=True),
    sa.CheckConstraint('record IS JSON', name='ck_pure_json_research_output_517_record'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_research_output_517')
    )
    op.create_table('pure_json_research_output_517_staging',
    sa.Column('record', sa.CLOB(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('modified', oracle.DATE(), nullable=False),
    sa.Column('downloaded', oracle.DATE(), nullable=True),
    sa.CheckConstraint('record IS JSON', name='ck_pure_json_research_output_517_staging_record'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_research_output_517_staging')
    )
