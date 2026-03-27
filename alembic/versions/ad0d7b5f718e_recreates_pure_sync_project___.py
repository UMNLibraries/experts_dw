"""Recreates pure_sync_project_*_participant tables, using award_id instead of project_id in the PKs

Revision ID: ad0d7b5f718e
Revises: 0d002c0e38dc
Create Date: 2026-03-27 13:22:14.880860

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'ad0d7b5f718e'
down_revision = '0d002c0e38dc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_sync_project_external_participant',
    sa.Column('project_id', sa.String(length=25), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('first_name', sa.String(length=1024), nullable=False),
    sa.Column('last_name', sa.String(length=1024), nullable=False),
    sa.Column('role', sa.String(length=15), nullable=False),
    sa.Column('award_id', sa.String(length=15), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['award_id'], ['pure_sync_award.award_id'], name=op.f('fk_pure_sync_project_external_participant_award_id_pure_sync_award')),
    sa.ForeignKeyConstraint(['project_id'], ['pure_sync_project.project_id'], name=op.f('fk_pure_sync_project_external_participant_project_id_pure_sync_project')),
    sa.PrimaryKeyConstraint('emplid', 'role', 'award_id', name=op.f('pk_pure_sync_project_external_participant'))
    )
    op.create_table('pure_sync_project_internal_participant',
    sa.Column('project_id', sa.String(length=25), nullable=True),
    sa.Column('person_id', sa.String(length=1024), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('organisation_id', sa.String(length=1024), nullable=False),
    sa.Column('role', sa.String(length=15), nullable=False),
    sa.Column('association_start_date', sa.DateTime(), nullable=True),
    sa.Column('association_end_date', sa.DateTime(), nullable=True),
    sa.Column('award_id', sa.String(length=15), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['award_id'], ['pure_sync_award.award_id'], name=op.f('fk_pure_sync_project_internal_participant_award_id_pure_sync_award')),
    sa.ForeignKeyConstraint(['project_id'], ['pure_sync_project.project_id'], name=op.f('fk_pure_sync_project_internal_participant_project_id_pure_sync_project')),
    sa.PrimaryKeyConstraint('person_id', 'role', 'award_id', name=op.f('pk_pure_sync_project_internal_participant'))
    )
    op.create_index(op.f('ix_pure_sync_project_internal_participant_emplid'), 'pure_sync_project_internal_participant', ['emplid'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_pure_sync_project_internal_participant_emplid'), table_name='pure_sync_project_internal_participant')
    op.drop_table('pure_sync_project_internal_participant')
    op.drop_table('pure_sync_project_external_participant')
