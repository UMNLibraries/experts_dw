"""Fixes nullability and other problems in pure_sync_(award|project)

Revision ID: b1ea2c370397
Revises: 03bf04fd7211
Create Date: 2026-03-26 13:02:57.104206

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'b1ea2c370397'
down_revision = '03bf04fd7211'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('pure_sync_award', sa.Column('short_title', sa.String(length=256), nullable=True))
    op.alter_column('pure_sync_award', 'award_date',
               existing_type=oracle.DATE(),
               nullable=False)
    op.alter_column('pure_sync_award', 'sponsor_award_number',
               existing_type=sa.VARCHAR(length=40),
               nullable=True)
    op.alter_column('pure_sync_award', 'financial_funding_id',
               existing_type=sa.VARCHAR(length=1024),
               nullable=True)
    op.drop_column('pure_sync_award', 'um_award_number')
    op.add_column('pure_sync_project', sa.Column('short_title', sa.String(length=256), nullable=True))
    op.alter_column('pure_sync_project', 'title',
               existing_type=sa.VARCHAR(length=256),
               type_=sa.String(length=1024),
               existing_nullable=False)
    op.alter_column('pure_sync_project', 'sponsor_award_number',
               existing_type=sa.VARCHAR(length=40),
               nullable=True)
    op.drop_column('pure_sync_project', 'um_award_number')
    op.drop_column('pure_sync_project', 'description')

def downgrade():
    op.add_column('pure_sync_project', sa.Column('description', sa.VARCHAR(length=1024), nullable=False))
    op.add_column('pure_sync_project', sa.Column('um_award_number', sa.VARCHAR(length=25), nullable=False))
    op.alter_column('pure_sync_project', 'sponsor_award_number',
               existing_type=sa.VARCHAR(length=40),
               nullable=False)
    op.alter_column('pure_sync_project', 'title',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=256),
               existing_nullable=False)
    op.drop_column('pure_sync_project', 'short_title')
    op.add_column('pure_sync_award', sa.Column('um_award_number', sa.VARCHAR(length=25), nullable=False))
    op.alter_column('pure_sync_award', 'financial_funding_id',
               existing_type=sa.VARCHAR(length=1024),
               nullable=False)
    op.alter_column('pure_sync_award', 'sponsor_award_number',
               existing_type=sa.VARCHAR(length=40),
               nullable=False)
    op.alter_column('pure_sync_award', 'award_date',
               existing_type=oracle.DATE(),
               nullable=True)
    op.drop_column('pure_sync_award', 'short_title')
