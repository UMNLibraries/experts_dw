"""Removes pure_sync_(award|project)* tables, so they can be re-created

Revision ID: 223173bea5a1
Revises: ca3fb5cb3a8e
Create Date: 2026-04-09 13:13:35.881882

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '223173bea5a1'
down_revision = 'ca3fb5cb3a8e'
branch_labels = None
depends_on = None

def upgrade():
    op.drop_index('ix_pure_sync_award_internal_holder_emplid', table_name='pure_sync_award_internal_holder')
    op.drop_table('pure_sync_award_internal_holder')
    op.drop_table('pure_sync_award_external_holder')
    op.drop_table('pure_sync_award')
    op.drop_index('ix_pure_sync_project_internal_participant_emplid', table_name='pure_sync_project_internal_participant')
    op.drop_table('pure_sync_project_internal_participant')
    op.drop_table('pure_sync_project_external_participant')
    op.drop_table('pure_sync_project')

def downgrade():
    op.create_table('pure_sync_award_external_holder',
    sa.Column('award_id', sa.VARCHAR(length=15), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('role', sa.VARCHAR(length=15), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.Column('updated', oracle.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['award_id'], ['pure_sync_award.award_id'], name='fk_pure_sync_award_external_holder_award_id_pure_sync_award'),
    sa.PrimaryKeyConstraint('award_id', 'emplid', 'role', name='pk_pure_sync_award_external_holder')
    )
    op.create_table('pure_sync_project',
    sa.Column('project_id', sa.VARCHAR(length=25), nullable=False),
    sa.Column('title', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('start_date', oracle.DATE(), nullable=True),
    sa.Column('end_date', oracle.DATE(), nullable=True),
    sa.Column('managed_by_organisation_id', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('managed_by_organisation_deptid', sa.VARCHAR(length=10), nullable=False),
    sa.Column('sponsor_award_number', sa.VARCHAR(length=40), nullable=True),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.Column('updated', oracle.DATE(), nullable=True),
    sa.Column('short_title', sa.VARCHAR(length=256), nullable=True),
    sa.PrimaryKeyConstraint('project_id', name='pk_pure_sync_project'),
    oracle_resolve_synonyms=False
    )
    op.create_table('pure_sync_project_internal_participant',
    sa.Column('project_id', sa.VARCHAR(length=25), nullable=False),
    sa.Column('person_id', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('organisation_id', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('role', sa.VARCHAR(length=15), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.Column('updated', oracle.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['pure_sync_project.project_id'], name='fk_pure_sync_project_internal_participant_project_id_pure_sync_project'),
    sa.PrimaryKeyConstraint('project_id', 'person_id', name='pk_pure_sync_project_internal_participant')
    )
    op.create_index('ix_pure_sync_project_internal_participant_emplid', 'pure_sync_project_internal_participant', ['emplid'], unique=False)
    op.create_table('pure_sync_award',
    sa.Column('award_id', sa.VARCHAR(length=15), nullable=False),
    sa.Column('title', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('actual_start_date', oracle.DATE(), nullable=True),
    sa.Column('actual_end_date', oracle.DATE(), nullable=True),
    sa.Column('award_date', oracle.DATE(), nullable=False),
    sa.Column('project_id', sa.VARCHAR(length=25), nullable=False),
    sa.Column('managed_by_organisation_id', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('managed_by_organisation_deptid', sa.VARCHAR(length=10), nullable=False),
    sa.Column('sponsor_award_number', sa.VARCHAR(length=40), nullable=True),
    sa.Column('primary_sponsor_award_number', sa.VARCHAR(length=40), nullable=True),
    sa.Column('financial_funding_id', sa.VARCHAR(length=1024), nullable=True),
    sa.Column('financial_funding_external_org_name', sa.VARCHAR(length=1024), nullable=True),
    sa.Column('financial_funding_primary_id', sa.VARCHAR(length=1024), nullable=True),
    sa.Column('financial_funding_primary_external_org_name', sa.VARCHAR(length=1024), nullable=True),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.Column('updated', oracle.DATE(), nullable=True),
    sa.Column('short_title', sa.VARCHAR(length=256), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['pure_sync_project.project_id'], name='fk_pure_sync_award_project_id_pure_sync_project'),
    sa.PrimaryKeyConstraint('award_id', name='pk_pure_sync_award'),
    oracle_resolve_synonyms=False
    )
    op.create_table('pure_sync_award_internal_holder',
    sa.Column('award_id', sa.VARCHAR(length=15), nullable=False),
    sa.Column('person_id', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('organisation_id', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('role', sa.VARCHAR(length=15), nullable=False),
    sa.Column('association_start_date', oracle.DATE(), nullable=True),
    sa.Column('association_end_date', oracle.DATE(), nullable=True),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.Column('updated', oracle.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['award_id'], ['pure_sync_award.award_id'], name='fk_pure_sync_award_internal_holder_award_id_pure_sync_award'),
    sa.ForeignKeyConstraint(['person_id'], ['pure_sync_person_data.person_id'], name='fk_pure_sync_award_internal_holder_person_id_pure_sync_person_data'),
    sa.PrimaryKeyConstraint('award_id', 'person_id', 'role', name='pk_pure_sync_award_internal_holder')
    )
    op.create_index('ix_pure_sync_award_internal_holder_emplid', 'pure_sync_award_internal_holder', ['emplid'], unique=False)
    op.create_table('pure_sync_project_external_participant',
    sa.Column('project_id', sa.VARCHAR(length=25), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('role', sa.VARCHAR(length=15), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.Column('updated', oracle.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['pure_sync_project.project_id'], name='fk_pure_sync_project_external_participant_project_id_pure_sync_project'),
    sa.PrimaryKeyConstraint('project_id', 'emplid', name='pk_pure_sync_project_external_participant')
    )
