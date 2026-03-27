"""Drops pure_sync_project_*_participant tables

Revision ID: 0d002c0e38dc
Revises: 2c9e534daf67
Create Date: 2026-03-27 13:15:29.560015

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '0d002c0e38dc'
down_revision = '2c9e534daf67'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('pure_sync_project_external_participant')
    op.drop_index('ix_pure_sync_project_internal_participant_emplid', table_name='pure_sync_project_internal_participant')
    op.drop_table('pure_sync_project_internal_participant')

def downgrade():
    op.create_table('pure_sync_project_internal_participant',
    sa.Column('project_id', sa.VARCHAR(length=25), nullable=False),
    sa.Column('person_id', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('organisation_id', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('role', sa.VARCHAR(length=15), nullable=False),
    sa.Column('association_start_date', oracle.DATE(), nullable=True),
    sa.Column('association_end_date', oracle.DATE(), nullable=True),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.Column('updated', oracle.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['pure_sync_project.project_id'], name='fk_pure_sync_project_internal_participant_project_id_pure_sync_project'),
    sa.PrimaryKeyConstraint('project_id', 'person_id', 'role', name='pk_pure_sync_project_internal_participant')
    )
    op.create_index('ix_pure_sync_project_internal_participant_emplid', 'pure_sync_project_internal_participant', ['emplid'], unique=False)
    op.create_table('pure_sync_project_external_participant',
    sa.Column('project_id', sa.VARCHAR(length=25), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('role', sa.VARCHAR(length=15), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.Column('updated', oracle.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['pure_sync_project.project_id'], name='fk_pure_sync_project_external_participant_project_id_pure_sync_project'),
    sa.PrimaryKeyConstraint('project_id', 'emplid', 'role', name='pk_pure_sync_project_external_participant')
    )
