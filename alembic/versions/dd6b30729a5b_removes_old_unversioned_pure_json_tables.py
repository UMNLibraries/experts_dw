"""Removes old unversioned pure_json* tables.

Revision ID: dd6b30729a5b
Revises: 646e9624a900
Create Date: 2020-09-28 10:45:14.406652

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'dd6b30729a5b'
down_revision = '646e9624a900'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('ck_pure_json_research_output_json', 'pure_json_research_output')
    op.drop_table('pure_json_research_output')
    op.drop_constraint('ck_pure_json_person_json', 'pure_json_person')
    op.drop_table('pure_json_person')
    op.drop_constraint('ck_pure_json_organisation_json', 'pure_json_organisation')
    op.drop_table('pure_json_organisation')

def downgrade():
    op.create_table('pure_json_organisation',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('json', sa.CLOB(), nullable=False),
    sa.Column('modified', oracle.DATE(), nullable=False),
    sa.Column('downloaded', oracle.DATE(), nullable=True),
    sa.CheckConstraint('JSON IS JSON', name='ck_pure_json_organisation_json'),
    sa.PrimaryKeyConstraint('uuid', name='sys_c00463897')
    )
    op.create_table('pure_json_person',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('json', sa.CLOB(), nullable=False),
    sa.Column('modified', oracle.DATE(), nullable=False),
    sa.Column('downloaded', oracle.DATE(), nullable=True),
    sa.CheckConstraint('JSON IS JSON', name='ck_pure_json_person_json'),
    sa.PrimaryKeyConstraint('uuid', name='sys_c00463901')
    )
    op.create_table('pure_json_research_output',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('json', sa.CLOB(), nullable=False),
    sa.Column('modified', oracle.DATE(), nullable=False),
    sa.Column('downloaded', oracle.DATE(), nullable=True),
    sa.CheckConstraint('JSON IS JSON', name='ck_pure_json_research_output_json'),
    sa.PrimaryKeyConstraint('uuid', name='sys_c00408019')
    )
