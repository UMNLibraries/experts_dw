"""Adds remaining pure_api_* tables.

Revision ID: 6b70db12a920
Revises: 438aa62fd7df
Create Date: 2018-07-23 14:46:20.252406

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '6b70db12a920'
down_revision = '438aa62fd7df'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_api_external_org',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('json', sa.Text(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'modified')
    )
    op.create_table('pure_api_external_org_hst',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=False),
    sa.Column('processed', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'modified')
    )
    op.create_table('pure_api_external_person',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('json', sa.Text(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'modified')
    )
    op.create_table('pure_api_external_person_hst',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=False),
    sa.Column('processed', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'modified')
    )
    op.create_table('pure_api_internal_org',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('json', sa.Text(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'modified')
    )
    op.create_table('pure_api_internal_org_hst',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=False),
    sa.Column('processed', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'modified')
    )
    op.create_table('pure_api_internal_person',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('json', sa.Text(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'modified')
    )
    op.create_table('pure_api_internal_person_hst',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=False),
    sa.Column('processed', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'modified')
    )


def downgrade():
    op.drop_table('pure_api_internal_person_hst')
    op.drop_table('pure_api_internal_person')
    op.drop_table('pure_api_internal_org_hst')
    op.drop_table('pure_api_internal_org')
    op.drop_table('pure_api_external_person_hst')
    op.drop_table('pure_api_external_person')
    op.drop_table('pure_api_external_org_hst')
    op.drop_table('pure_api_external_org')
