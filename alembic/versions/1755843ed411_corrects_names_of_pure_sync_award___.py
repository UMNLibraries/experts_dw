"""Corrects names of pure_sync_award_*_holder date columns

Revision ID: 1755843ed411
Revises: d5e8e9985d0b
Create Date: 2026-03-27 08:09:33.790654

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '1755843ed411'
down_revision = 'd5e8e9985d0b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('pure_sync_award_external_holder', sa.Column('inserted', sa.DateTime(), nullable=True))
    op.add_column('pure_sync_award_external_holder', sa.Column('updated', sa.DateTime(), nullable=True))
    op.drop_column('pure_sync_award_external_holder', 'modified')
    op.drop_column('pure_sync_award_external_holder', 'created')
    op.add_column('pure_sync_award_internal_holder', sa.Column('inserted', sa.DateTime(), nullable=True))
    op.add_column('pure_sync_award_internal_holder', sa.Column('updated', sa.DateTime(), nullable=True))
    op.drop_column('pure_sync_award_internal_holder', 'modified')
    op.drop_column('pure_sync_award_internal_holder', 'created')

def downgrade():
    op.add_column('pure_sync_award_internal_holder', sa.Column('created', oracle.DATE(), nullable=True))
    op.add_column('pure_sync_award_internal_holder', sa.Column('modified', oracle.DATE(), nullable=True))
    op.drop_column('pure_sync_award_internal_holder', 'updated')
    op.drop_column('pure_sync_award_internal_holder', 'inserted')
    op.add_column('pure_sync_award_external_holder', sa.Column('created', oracle.DATE(), nullable=True))
    op.add_column('pure_sync_award_external_holder', sa.Column('modified', oracle.DATE(), nullable=True))
    op.drop_column('pure_sync_award_external_holder', 'updated')
    op.drop_column('pure_sync_award_external_holder', 'inserted')
