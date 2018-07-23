"""Adds pure_api_change(_hst)?

Revision ID: 438aa62fd7df
Revises: 00794c908caa
Create Date: 2018-07-23 14:34:57.783206

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '438aa62fd7df'
down_revision = '00794c908caa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_api_change',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('json', sa.Text(), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'version')
    )
    op.create_table('pure_api_change_hst',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=False),
    sa.Column('processed', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'version')
    )


def downgrade():
    op.drop_table('pure_api_change_hst')
    op.drop_table('pure_api_change')
