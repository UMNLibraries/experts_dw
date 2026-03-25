"""Adds index to pure_sync_person_data.emplid

Revision ID: c4799d3014e5
Revises: 053d0ff8e6a6
Create Date: 2026-03-18 13:32:54.230577

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'c4799d3014e5'
down_revision = '053d0ff8e6a6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(op.f('ix_pure_sync_person_data_emplid'), 'pure_sync_person_data', ['emplid'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_pure_sync_person_data_emplid'), table_name='pure_sync_person_data')
