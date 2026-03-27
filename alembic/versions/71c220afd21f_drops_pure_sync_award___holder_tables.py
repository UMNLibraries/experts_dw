"""Drops pure_sync_award_*_holder tables

Revision ID: 71c220afd21f
Revises: 1755843ed411
Create Date: 2026-03-27 09:25:30.723308

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '71c220afd21f'
down_revision = '1755843ed411'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('pure_sync_award_external_holder')
    op.drop_index('ix_pure_sync_award_internal_holder_emplid', table_name='pure_sync_award_internal_holder')
    op.drop_table('pure_sync_award_internal_holder')

def downgrade():
    op.create_table('pure_sync_award_internal_holder',
    sa.Column('award_id', sa.VARCHAR(length=15), nullable=False),
    sa.Column('person_id', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('organisation_id', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('role', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.Column('updated', oracle.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['award_id'], ['pure_sync_award.award_id'], name='fk_pure_sync_award_internal_holder_award_id_pure_sync_award'),
    sa.ForeignKeyConstraint(['person_id'], ['pure_sync_person_data.person_id'], name='fk_pure_sync_award_internal_holder_person_id_pure_sync_person_data'),
    sa.PrimaryKeyConstraint('award_id', 'person_id', name='pk_pure_sync_award_internal_holder')
    )
    op.create_index('ix_pure_sync_award_internal_holder_emplid', 'pure_sync_award_internal_holder', ['emplid'], unique=False)
    op.create_table('pure_sync_award_external_holder',
    sa.Column('award_id', sa.VARCHAR(length=15), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('last_name', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('role', sa.VARCHAR(length=1024), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=True),
    sa.Column('updated', oracle.DATE(), nullable=True),
    sa.ForeignKeyConstraint(['award_id'], ['pure_sync_award.award_id'], name='fk_pure_sync_award_external_holder_award_id_pure_sync_award'),
    sa.PrimaryKeyConstraint('award_id', 'emplid', name='pk_pure_sync_award_external_holder')
    )
