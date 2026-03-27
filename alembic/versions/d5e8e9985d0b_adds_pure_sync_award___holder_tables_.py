"""Adds pure_sync_award_*_holder tables, reduces sizes of some pure_sync* keys

Revision ID: d5e8e9985d0b
Revises: b1ea2c370397
Create Date: 2026-03-27 07:49:07.640746

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'd5e8e9985d0b'
down_revision = 'b1ea2c370397'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_sync_award_external_holder',
    sa.Column('award_id', sa.String(length=15), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('first_name', sa.String(length=1024), nullable=False),
    sa.Column('last_name', sa.String(length=1024), nullable=False),
    sa.Column('role', sa.String(length=1024), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['award_id'], ['pure_sync_award.award_id'], name=op.f('fk_pure_sync_award_external_holder_award_id_pure_sync_award')),
    sa.PrimaryKeyConstraint('award_id', 'emplid', name=op.f('pk_pure_sync_award_external_holder'))
    )
    op.create_table('pure_sync_award_internal_holder',
    sa.Column('award_id', sa.String(length=15), nullable=False),
    sa.Column('person_id', sa.String(length=1024), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('organisation_id', sa.String(length=1024), nullable=False),
    sa.Column('role', sa.String(length=1024), nullable=False),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['award_id'], ['pure_sync_award.award_id'], name=op.f('fk_pure_sync_award_internal_holder_award_id_pure_sync_award')),
    sa.ForeignKeyConstraint(['person_id'], ['pure_sync_person_data.person_id'], name=op.f('fk_pure_sync_award_internal_holder_person_id_pure_sync_person_data')),
    sa.PrimaryKeyConstraint('award_id', 'person_id', name=op.f('pk_pure_sync_award_internal_holder'))
    )
    op.create_index(op.f('ix_pure_sync_award_internal_holder_emplid'), 'pure_sync_award_internal_holder', ['emplid'], unique=False)
    op.alter_column('pure_sync_award', 'award_id',
               existing_type=sa.VARCHAR(length=1024),
               type_=sa.String(length=15),
               existing_nullable=False)
    op.alter_column('pure_sync_award', 'project_id',
               existing_type=sa.VARCHAR(length=1024),
               type_=sa.String(length=25),
               existing_nullable=False)
    op.alter_column('pure_sync_project', 'project_id',
               existing_type=sa.VARCHAR(length=1024),
               type_=sa.String(length=25),
               existing_nullable=False)

def downgrade():
    op.alter_column('pure_sync_project', 'project_id',
               existing_type=sa.String(length=25),
               type_=sa.VARCHAR(length=1024),
               existing_nullable=False)
    op.alter_column('pure_sync_award', 'project_id',
               existing_type=sa.String(length=25),
               type_=sa.VARCHAR(length=1024),
               existing_nullable=False)
    op.alter_column('pure_sync_award', 'award_id',
               existing_type=sa.String(length=15),
               type_=sa.VARCHAR(length=1024),
               existing_nullable=False)
    op.drop_index(op.f('ix_pure_sync_award_internal_holder_emplid'), table_name='pure_sync_award_internal_holder')
    op.drop_table('pure_sync_award_internal_holder')
    op.drop_table('pure_sync_award_external_holder')
    op.drop_table('pure_eligible_graduate_program')
