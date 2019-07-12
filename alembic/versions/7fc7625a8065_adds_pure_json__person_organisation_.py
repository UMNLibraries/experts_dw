"""Adds pure_json_(person|organisation) tables.

Revision ID: 7fc7625a8065
Revises: 9eeb06c042b2
Create Date: 2019-07-09 07:53:26.344448

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '7fc7625a8065'
down_revision = '9eeb06c042b2'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('pure_json_organisation',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('json', sa.Text(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table('pure_json_person',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('json', sa.Text(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
    )

def downgrade():
    op.drop_table('pure_json_person')
    op.drop_table('pure_json_organisation')
