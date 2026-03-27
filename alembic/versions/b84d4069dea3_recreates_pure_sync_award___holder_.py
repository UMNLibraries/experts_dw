"""Recreates pure_sync_award_*_holder tables, adding role to the PKs, and some dates to internal holders

Revision ID: b84d4069dea3
Revises: 64b526f5d4b0
Create Date: 2026-03-27 09:49:01.519123

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'b84d4069dea3'
down_revision = '64b526f5d4b0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_sync_award_external_holder',
    sa.Column('award_id', sa.String(length=15), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('first_name', sa.String(length=1024), nullable=False),
    sa.Column('last_name', sa.String(length=1024), nullable=False),
    sa.Column('role', sa.String(length=15), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['award_id'], ['pure_sync_award.award_id'], name=op.f('fk_pure_sync_award_external_holder_award_id_pure_sync_award')),
    sa.PrimaryKeyConstraint('award_id', 'emplid', 'role', name=op.f('pk_pure_sync_award_external_holder'))
    )
    op.create_table('pure_sync_award_internal_holder',
    sa.Column('award_id', sa.String(length=15), nullable=False),
    sa.Column('person_id', sa.String(length=1024), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('organisation_id', sa.String(length=1024), nullable=False),
    sa.Column('role', sa.String(length=15), nullable=False),
    sa.Column('association_start_date', sa.DateTime(), nullable=True),
    sa.Column('association_end_date', sa.DateTime(), nullable=True),
    sa.Column('inserted', sa.DateTime(), nullable=True),
    sa.Column('updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['award_id'], ['pure_sync_award.award_id'], name=op.f('fk_pure_sync_award_internal_holder_award_id_pure_sync_award')),
    sa.ForeignKeyConstraint(['person_id'], ['pure_sync_person_data.person_id'], name=op.f('fk_pure_sync_award_internal_holder_person_id_pure_sync_person_data')),
    sa.PrimaryKeyConstraint('award_id', 'person_id', 'role', name=op.f('pk_pure_sync_award_internal_holder'))
    )
    op.create_index(op.f('ix_pure_sync_award_internal_holder_emplid'), 'pure_sync_award_internal_holder', ['emplid'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_pure_sync_award_internal_holder_emplid'), table_name='pure_sync_award_internal_holder')
    op.drop_table('pure_sync_award_internal_holder')
    op.drop_table('pure_sync_award_external_holder')
