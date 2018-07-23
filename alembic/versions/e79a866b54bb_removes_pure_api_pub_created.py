"""Removes pure_api_pub.created.

Revision ID: e79a866b54bb
Revises: 8562b82ae686
Create Date: 2018-07-23 13:58:53.713574

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'e79a866b54bb'
down_revision = '8562b82ae686'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('pure_api_pub', 'created')

def downgrade():
    op.add_column('pure_api_pub', sa.Column('created', oracle.DATE(), nullable=False))
