"""Adds pure_json_collection_meta table.

Revision ID: edeb7133b093
Revises: d2a6a03e4c73
Create Date: 2020-11-10 12:22:04.523444

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'edeb7133b093'
down_revision = 'd2a6a03e4c73'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_json_collection_meta',
    sa.Column('api_name', sa.String(length=255), nullable=False, comment='Name of the collection in the Pure API, i.e., in URL endpoints.'),
    sa.Column('api_version', sa.String(length=15), nullable=False, comment='The Pure API version, without the decimal point, i.e., 516 for version 5.16.'),
    sa.Column('family_system_name', sa.String(length=255), nullable=False, comment='Name of the collection in API change records, where it is called familySystemName.'),
    sa.Column('local_name', sa.String(length=255), nullable=False, comment='Name of the collection as it appears in local table names.'),
    sa.PrimaryKeyConstraint('api_name', 'api_version', 'family_system_name', 'local_name', name=op.f('pk_pure_json_collection_meta')),
    comment='Maps Pure API collection names, family system names, and versions to local table names.'
    )

def downgrade():
    op.drop_table('pure_json_collection_meta')
