"""Adds pure_sync_award and pure_sync_project tables

Revision ID: 03bf04fd7211
Revises: 0e1172dba51b
Create Date: 2026-03-24 14:22:27.377795

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '03bf04fd7211'
down_revision = '0e1172dba51b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_sync_project',
    sa.Column('project_id', sa.String(length=1024), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('description', sa.String(length=1024), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('managed_by_organisation_id', sa.String(length=1024), nullable=False),
    sa.Column('managed_by_organisation_deptid', sa.String(length=10), nullable=False),
    sa.Column('um_award_number', sa.String(length=25), nullable=False),
    sa.Column('sponsor_award_number', sa.String(length=40), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('project_id', name=op.f('pk_pure_sync_project'))
    )
    op.create_table('pure_sync_award',
    sa.Column('award_id', sa.String(length=1024), nullable=False),
    sa.Column('title', sa.String(length=1024), nullable=False),
    sa.Column('actual_start_date', sa.DateTime(), nullable=True),
    sa.Column('actual_end_date', sa.DateTime(), nullable=True),
    sa.Column('award_date', sa.DateTime(), nullable=True),
    sa.Column('project_id', sa.String(length=1024), nullable=False),
    sa.Column('managed_by_organisation_id', sa.String(length=1024), nullable=False),
    sa.Column('managed_by_organisation_deptid', sa.String(length=10), nullable=False),
    sa.Column('um_award_number', sa.String(length=25), nullable=False),
    sa.Column('sponsor_award_number', sa.String(length=40), nullable=False),
    sa.Column('primary_sponsor_award_number', sa.String(length=40), nullable=True),
    sa.Column('financial_funding_id', sa.String(length=1024), nullable=False),
    sa.Column('financial_funding_external_org_name', sa.String(length=1024), nullable=True),
    sa.Column('financial_funding_primary_id', sa.String(length=1024), nullable=True),
    sa.Column('financial_funding_primary_external_org_name', sa.String(length=1024), nullable=True),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['pure_sync_project.project_id'], name=op.f('fk_pure_sync_award_project_id_pure_sync_project')),
    sa.PrimaryKeyConstraint('award_id', name=op.f('pk_pure_sync_award'))
    )

def downgrade():
    op.drop_table('pure_sync_award')
    op.drop_table('pure_sync_project')
