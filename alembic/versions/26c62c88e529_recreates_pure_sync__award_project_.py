"""Recreates pure_sync_(award|project)* tables, with improved representation of UMN data

Revision ID: 26c62c88e529
Revises: 223173bea5a1
Create Date: 2026-04-09 13:33:07.813211

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '26c62c88e529'
down_revision = '223173bea5a1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_sync_project',
    sa.Column('project_id', sa.String(length=25), nullable=False),
    sa.Column('title', sa.String(length=1024), nullable=False),
    sa.Column('short_title', sa.String(length=256), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('managed_by_organisation_id', sa.String(length=1024), nullable=False),
    sa.Column('managed_by_organisation_deptid', sa.String(length=10), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('project_id', name=op.f('pk_pure_sync_project'))
    )
    op.create_table('pure_sync_award',
    sa.Column('award_id', sa.String(length=25), nullable=False),
    sa.Column('title', sa.String(length=1024), nullable=False),
    sa.Column('short_title', sa.String(length=256), nullable=True),
    sa.Column('actual_start_date', sa.DateTime(), nullable=True),
    sa.Column('actual_end_date', sa.DateTime(), nullable=True),
    sa.Column('award_date', sa.DateTime(), nullable=False),
    sa.Column('project_id', sa.String(length=25), nullable=False),
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
    op.create_table('pure_sync_project_external_participant',
    sa.Column('project_id', sa.String(length=25), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('first_name', sa.String(length=1024), nullable=False),
    sa.Column('last_name', sa.String(length=1024), nullable=False),
    sa.Column('role', sa.String(length=15), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['pure_sync_project.project_id'], name=op.f('fk_pure_sync_project_external_participant_project_id_pure_sync_project')),
    sa.PrimaryKeyConstraint('project_id', 'emplid', name=op.f('pk_pure_sync_project_external_participant'))
    )
    op.create_table('pure_sync_project_internal_participant',
    sa.Column('project_id', sa.String(length=25), nullable=False),
    sa.Column('person_id', sa.String(length=1024), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('organisation_id', sa.String(length=1024), nullable=False),
    sa.Column('role', sa.String(length=15), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['pure_sync_project.project_id'], name=op.f('fk_pure_sync_project_internal_participant_project_id_pure_sync_project')),
    sa.PrimaryKeyConstraint('project_id', 'person_id', name=op.f('pk_pure_sync_project_internal_participant'))
    )
    op.create_index(op.f('ix_pure_sync_project_internal_participant_emplid'), 'pure_sync_project_internal_participant', ['emplid'], unique=False)
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
    op.drop_index(op.f('ix_pure_sync_project_internal_participant_emplid'), table_name='pure_sync_project_internal_participant')
    op.drop_table('pure_sync_project_internal_participant')
    op.drop_table('pure_sync_project_external_participant')
    op.drop_index(op.f('ix_pure_sync_award_emplid'), table_name='pure_sync_award')
    op.drop_table('pure_sync_award')
    op.drop_table('pure_sync_project')
