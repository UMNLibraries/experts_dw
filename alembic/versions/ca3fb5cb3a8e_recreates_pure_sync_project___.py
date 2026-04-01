"""Recreates pure_sync_project_*_participant tables, replacing role & award_id with project_id in PKs

Revision ID: ca3fb5cb3a8e
Revises: 2821a65ebe4a
Create Date: 2026-04-01 09:01:19.909461

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'ca3fb5cb3a8e'
down_revision = '2821a65ebe4a'
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

def downgrade():
    op.drop_index(op.f('ix_pure_sync_project_internal_participant_emplid'), table_name='pure_sync_project_internal_participant')
    op.drop_table('pure_sync_project_internal_participant')
    op.drop_table('pure_sync_project_external_participant')
