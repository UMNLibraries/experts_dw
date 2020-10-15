"""Adds a pure_json_research_output_previous_uuid table.

Revision ID: aea6a3aad4a4
Revises: 3066f3c72ecf
Create Date: 2020-10-09 08:24:15.057409

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'aea6a3aad4a4'
down_revision = '3066f3c72ecf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_json_research_output_previous_uuid',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('previous_uuid', sa.String(length=36), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'previous_uuid', name=op.f('pk_pure_json_research_output_previous_uuid'))
    )

def downgrade():
    op.drop_table('pure_json_research_output_previous_uuid')
