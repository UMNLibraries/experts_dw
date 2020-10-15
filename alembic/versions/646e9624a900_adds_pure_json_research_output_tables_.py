"""Adds pure_json_research_output* tables with support for multiple versions.

Revision ID: 646e9624a900
Revises: d3168b930efb
Create Date: 2020-09-22 14:04:15.974989

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '646e9624a900'
down_revision = 'd3168b930efb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_json_research_output_516',
    sa.Column('record', sa.Text(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=True),
    sa.CheckConstraint('record IS JSON', name=op.f('ck_pure_json_research_output_516_record')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_research_output_516'))
    )
    op.create_table('pure_json_research_output_516_staging',
    sa.Column('record', sa.Text(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=True),
    sa.CheckConstraint('record IS JSON', name=op.f('ck_pure_json_research_output_516_staging_record')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_research_output_516_staging'))
    )
    op.create_table('pure_json_research_output_517',
    sa.Column('record', sa.Text(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=True),
    sa.CheckConstraint('record IS JSON', name=op.f('ck_pure_json_research_output_517_record')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_research_output_517'))
    )
    op.create_table('pure_json_research_output_517_staging',
    sa.Column('record', sa.Text(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=True),
    sa.CheckConstraint('record IS JSON', name=op.f('ck_pure_json_research_output_517_staging_record')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_research_output_517_staging'))
    )

def downgrade():
    op.drop_table('pure_json_research_output_517_staging')
    op.drop_table('pure_json_research_output_517')
    op.drop_table('pure_json_research_output_516_staging')
    op.drop_table('pure_json_research_output_516')
