"""Recreates pure_sync_award* tables, with previously missing columns

Revision ID: 2dd9f4b91c45
Revises: 68e140bca6ac
Create Date: 2026-04-09 14:03:03.506920

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '2dd9f4b91c45'
down_revision = '68e140bca6ac'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_sync_award',
    sa.Column('award_id', sa.String(length=25), nullable=False),
    sa.Column('title', sa.String(length=1024), nullable=False),
    sa.Column('short_title', sa.String(length=256), nullable=True),
    sa.Column('actual_start_date', sa.DateTime(), nullable=True),
    sa.Column('actual_end_date', sa.DateTime(), nullable=True),
    sa.Column('award_date', sa.DateTime(), nullable=False),
    sa.Column('project_id', sa.String(length=25), nullable=False),
    sa.Column('umn_award_contract_number', sa.String(length=25), nullable=False),
    sa.Column('umn_previous_award_contract_number', sa.String(length=25), nullable=True),
    sa.Column('managed_by_organisation_id', sa.String(length=1024), nullable=False),
    sa.Column('managed_by_organisation_deptid', sa.String(length=10), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('sponsor_award_number', sa.String(length=40), nullable=True),
    sa.Column('primary_sponsor_award_number', sa.String(length=40), nullable=True),
    sa.Column('federal_award_number', sa.String(length=50), nullable=True),
    sa.Column('financial_funding_id', sa.String(length=1024), nullable=True),
    sa.Column('financial_funding_external_org_name', sa.String(length=1024), nullable=True),
    sa.Column('financial_funding_primary_id', sa.String(length=1024), nullable=True),
    sa.Column('financial_funding_primary_external_org_name', sa.String(length=1024), nullable=True),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['pure_sync_project.project_id'], name=op.f('fk_pure_sync_award_project_id_pure_sync_project')),
    sa.PrimaryKeyConstraint('award_id', name=op.f('pk_pure_sync_award'))
    )
    op.create_index(op.f('ix_pure_sync_award_emplid'), 'pure_sync_award', ['emplid'], unique=False)
    op.create_table('pure_sync_award_external_holder',
    sa.Column('award_id', sa.String(length=25), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('first_name', sa.String(length=1024), nullable=False),
    sa.Column('last_name', sa.String(length=1024), nullable=False),
    sa.Column('role', sa.String(length=15), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['award_id'], ['pure_sync_award.award_id'], name=op.f('fk_pure_sync_award_external_holder_award_id_pure_sync_award')),
    sa.PrimaryKeyConstraint('award_id', 'emplid', name=op.f('pk_pure_sync_award_external_holder'))
    )
    op.create_table('pure_sync_award_internal_holder',
    sa.Column('award_id', sa.String(length=25), nullable=False),
    sa.Column('person_id', sa.String(length=1024), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('organisation_id', sa.String(length=1024), nullable=False),
    sa.Column('role', sa.String(length=15), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['award_id'], ['pure_sync_award.award_id'], name=op.f('fk_pure_sync_award_internal_holder_award_id_pure_sync_award')),
    sa.ForeignKeyConstraint(['person_id'], ['pure_sync_person_data.person_id'], name=op.f('fk_pure_sync_award_internal_holder_person_id_pure_sync_person_data')),
    sa.PrimaryKeyConstraint('award_id', 'person_id', name=op.f('pk_pure_sync_award_internal_holder'))
    )
    op.create_index(op.f('ix_pure_sync_award_internal_holder_emplid'), 'pure_sync_award_internal_holder', ['emplid'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_pure_sync_award_internal_holder_emplid'), table_name='pure_sync_award_internal_holder')
    op.drop_table('pure_sync_award_internal_holder')
    op.drop_table('pure_sync_award_external_holder')
    op.drop_index(op.f('ix_pure_sync_award_emplid'), table_name='pure_sync_award')
    op.drop_table('pure_sync_award')
