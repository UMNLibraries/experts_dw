"""Adds pure_json_research_output table.

Revision ID: 960fc1e68982
Revises: 9a7c302f1949
Create Date: 2019-05-13 13:46:47.901534

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '960fc1e68982'
down_revision = '9a7c302f1949'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_json_research_output',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('json', sa.Text(), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=True),
    sa.CheckConstraint('JSON IS JSON'),
    sa.PrimaryKeyConstraint('uuid')
    )

def downgrade():
    op.drop_table('pure_json_research_output')
