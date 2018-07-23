"""Adds pure_api_pub_hst.

Revision ID: 00794c908caa
Revises: e79a866b54bb
Create Date: 2018-07-23 14:20:03.398526

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '00794c908caa'
down_revision = 'e79a866b54bb'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_api_pub_hst',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=False),
    sa.Column('processed', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'modified')
    )


def downgrade():
    op.drop_table('pure_api_pub_hst')
