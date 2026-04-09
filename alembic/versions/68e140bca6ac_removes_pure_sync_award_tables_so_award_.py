"""Removes pure_sync_award* tables, so award can be re-created with now-missing columns

Revision ID: 68e140bca6ac
Revises: 26c62c88e529
Create Date: 2026-04-09 13:57:02.068507

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '68e140bca6ac'
down_revision = '26c62c88e529'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_index('ix_pure_sync_award_internal_holder_emplid', table_name='pure_sync_award_internal_holder')
    op.drop_table('pure_sync_award_internal_holder')
    op.drop_table('pure_sync_award_external_holder')
    op.drop_index('ix_pure_sync_award_emplid', table_name='pure_sync_award')
    op.drop_table('pure_sync_award')

def downgrade():
    op.create_table('pure_sync_award_external_holder',
    sa.Column('award_id', sa.VARCHAR(length=25), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('role', sa.VARCHAR(length=15), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.Column('updated', oracle.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['award_id'], ['pure_sync_award.award_id'], name='fk_pure_sync_award_external_holder_award_id_pure_sync_award'),
    sa.PrimaryKeyConstraint('award_id', 'emplid', name='pk_pure_sync_award_external_holder')
    )
    op.create_table('pure_sync_award',
    sa.Column('award_id', sa.VARCHAR(length=25), nullable=False),
    sa.Column('title', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('short_title', sa.VARCHAR(length=256), nullable=True),
    sa.Column('actual_start_date', oracle.DATE(), nullable=True),
    sa.Column('actual_end_date', oracle.DATE(), nullable=True),
    sa.Column('award_date', oracle.DATE(), nullable=False),
    sa.Column('project_id', sa.VARCHAR(length=25), nullable=False),
    sa.Column('managed_by_organisation_id', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('managed_by_organisation_deptid', sa.VARCHAR(length=10), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('sponsor_award_number', sa.VARCHAR(length=40), nullable=True),
    sa.Column('primary_sponsor_award_number', sa.VARCHAR(length=40), nullable=True),
    sa.Column('federal_award_number', sa.VARCHAR(length=50), nullable=True),
    sa.Column('financial_funding_id', sa.VARCHAR(length=1024), nullable=True),
    sa.Column('financial_funding_external_org_name', sa.VARCHAR(length=1024), nullable=True),
    sa.Column('financial_funding_primary_id', sa.VARCHAR(length=1024), nullable=True),
    sa.Column('financial_funding_primary_external_org_name', sa.VARCHAR(length=1024), nullable=True),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.Column('updated', oracle.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['pure_sync_project.project_id'], name='fk_pure_sync_award_project_id_pure_sync_project'),
    sa.PrimaryKeyConstraint('award_id', name='pk_pure_sync_award'),
    oracle_resolve_synonyms=False
    )
    op.create_index('ix_pure_sync_award_emplid', 'pure_sync_award', ['emplid'], unique=False)
    op.create_table('pure_sync_award_internal_holder',
    sa.Column('award_id', sa.VARCHAR(length=25), nullable=False),
    sa.Column('person_id', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('organisation_id', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('role', sa.VARCHAR(length=15), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.Column('updated', oracle.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['award_id'], ['pure_sync_award.award_id'], name='fk_pure_sync_award_internal_holder_award_id_pure_sync_award'),
    sa.ForeignKeyConstraint(['person_id'], ['pure_sync_person_data.person_id'], name='fk_pure_sync_award_internal_holder_person_id_pure_sync_person_data'),
    sa.PrimaryKeyConstraint('award_id', 'person_id', name='pk_pure_sync_award_internal_holder')
    )
    op.create_index('ix_pure_sync_award_internal_holder_emplid', 'pure_sync_award_internal_holder', ['emplid'], unique=False)
