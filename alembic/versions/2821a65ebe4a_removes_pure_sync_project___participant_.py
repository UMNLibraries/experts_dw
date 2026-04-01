"""Removes pure_sync_project_*_participant tables

Revision ID: 2821a65ebe4a
Revises: ad0d7b5f718e
Create Date: 2026-04-01 08:52:37.486828

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '2821a65ebe4a'
down_revision = 'ad0d7b5f718e'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('pure_sync_project_external_participant')
    op.drop_index('ix_pure_sync_project_internal_participant_emplid', table_name='pure_sync_project_internal_participant')
    op.drop_table('pure_sync_project_internal_participant')

def downgrade():
    op.create_table('pure_sync_project_internal_participant',
    sa.ForeignKeyConstraint(['award_id'], ['pure_sync_award.award_id'], name='fk_pure_sync_project_internal_participant_award_id_pure_sync_award'),
    sa.ForeignKeyConstraint(['project_id'], ['pure_sync_project.project_id'], name='fk_pure_sync_project_internal_participant_project_id_pure_sync_project'),
    sa.PrimaryKeyConstraint('person_id', 'role', 'award_id', name='pk_pure_sync_project_internal_participant')
    )
    op.create_index('ix_pure_sync_project_internal_participant_emplid', 'pure_sync_project_internal_participant', ['emplid'], unique=False)
    op.create_table('pure_sync_project_external_participant',
    sa.Column('project_id', sa.VARCHAR(length=25), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('role', sa.VARCHAR(length=15), nullable=False),
    sa.Column('award_id', sa.VARCHAR(length=15), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.Column('updated', oracle.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['award_id'], ['pure_sync_award.award_id'], name='fk_pure_sync_project_external_participant_award_id_pure_sync_award'),
    sa.ForeignKeyConstraint(['project_id'], ['pure_sync_project.project_id'], name='fk_pure_sync_project_external_participant_project_id_pure_sync_project'),
    sa.PrimaryKeyConstraint('emplid', 'role', 'award_id', name='pk_pure_sync_project_external_participant')
    )
