"""Adds index to pure_sync_staff_org_association.person_id

Revision ID: 0e1172dba51b
Revises: c4799d3014e5
Create Date: 2026-03-18 14:43:14.873617

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '0e1172dba51b'
down_revision = 'c4799d3014e5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(op.f('ix_pure_sync_staff_org_association_person_id'), 'pure_sync_staff_org_association', ['person_id'], unique=False)

def downgrade():
    op.drop_index(op.f('ix_pure_sync_staff_org_association_person_id'), table_name='pure_sync_staff_org_association')
