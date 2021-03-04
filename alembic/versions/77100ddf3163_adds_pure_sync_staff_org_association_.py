"""Adds pure_sync_staff_org_association*.email_address.

Revision ID: 77100ddf3163
Revises: 503096bbd562
Create Date: 2021-03-04 16:23:55.793880

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '77100ddf3163'
down_revision = '503096bbd562'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('pure_sync_staff_org_association', sa.Column('email_address', sa.String(length=255), nullable=True))
    op.add_column('pure_sync_staff_org_association_scratch', sa.Column('email_address', sa.String(length=255), nullable=True))

def downgrade():
    op.drop_column('pure_sync_staff_org_association_scratch', 'email_address')
    op.drop_column('pure_sync_staff_org_association', 'email_address')
