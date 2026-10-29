"""Adds pure_json_change_524_history_archive table

Revision ID: b4819b11ead7
Revises: 2dd9f4b91c45
Create Date: 2026-10-13 13:46:22.514669

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'b4819b11ead7'
down_revision = '2dd9f4b91c45'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_json_change_524_history_archive',
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('pure_version', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'pure_version', name=op.f('pk_pure_json_change_524_history_archive'))
    )

def downgrade():
    op.drop_table('pure_json_change_524_history_archive')
