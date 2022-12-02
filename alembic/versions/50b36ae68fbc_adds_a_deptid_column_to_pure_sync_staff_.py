"""Adds a deptid column to pure_sync_staff_org_association tables.

Revision ID: 50b36ae68fbc
Revises: 6bb8ebdfbbcd
Create Date: 2022-12-02 13:45:54.606880

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '50b36ae68fbc'
down_revision = '6bb8ebdfbbcd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('pure_sync_staff_org_association', sa.Column('deptid', sa.String(length=10), nullable=True))
    op.add_column('pure_sync_staff_org_association_scratch', sa.Column('deptid', sa.String(length=10), nullable=True))


def downgrade():
    op.drop_column('pure_sync_staff_org_association_scratch', 'deptid')
    op.drop_column('pure_sync_staff_org_association', 'deptid')
