"""Adds pure_sync_staff_org_association.affiliation_idw.

Revision ID: 7d50429f27a7
Revises: db5763dbc150
Create Date: 2019-03-12 13:43:50.801655

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '7d50429f27a7'
down_revision = 'db5763dbc150'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('pure_sync_staff_org_association', sa.Column('affiliation_id', sa.String(length=30), nullable=True))

def downgrade():
    op.drop_column('pure_sync_staff_org_association', 'affiliation_id')
