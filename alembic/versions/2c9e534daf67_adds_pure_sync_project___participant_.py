"""Adds pure_sync_project_*_participant tables

Revision ID: 2c9e534daf67
Revises: b84d4069dea3
Create Date: 2026-03-27 12:39:28.276328

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '2c9e534daf67'
down_revision = 'b84d4069dea3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_sync_project_external_participant',
    sa.Column('project_id', sa.String(length=25), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('first_name', sa.String(length=1024), nullable=False),
    sa.Column('last_name', sa.String(length=1024), nullable=False),
    sa.Column('role', sa.String(length=15), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['pure_sync_project.project_id'], name=op.f('fk_pure_sync_project_external_participant_project_id_pure_sync_project')),
    sa.PrimaryKeyConstraint('project_id', 'emplid', 'role', name=op.f('pk_pure_sync_project_external_participant'))
    )
    op.create_table('pure_sync_project_internal_participant',
    sa.Column('project_id', sa.String(length=25), nullable=False),
    sa.Column('person_id', sa.String(length=1024), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('organisation_id', sa.String(length=1024), nullable=False),
    sa.Column('role', sa.String(length=15), nullable=False),
    sa.Column('association_start_date', sa.DateTime(), nullable=True),
    sa.Column('association_end_date', sa.DateTime(), nullable=True),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['project_id'], ['pure_sync_project.project_id'], name=op.f('fk_pure_sync_project_internal_participant_project_id_pure_sync_project')),
    sa.PrimaryKeyConstraint('project_id', 'person_id', 'role', name=op.f('pk_pure_sync_project_internal_participant'))
    )
    op.create_index(op.f('ix_pure_sync_project_internal_participant_emplid'), 'pure_sync_project_internal_participant', ['emplid'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_pure_sync_project_internal_participant_emplid'), table_name='pure_sync_project_internal_participant')
    op.drop_table('pure_sync_project_internal_participant')
    op.drop_table('pure_sync_project_external_participant')
