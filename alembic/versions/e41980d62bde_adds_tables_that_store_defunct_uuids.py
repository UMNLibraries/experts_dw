"""Adds tables that store defunct uuids

Revision ID: e41980d62bde
Revises: 4e6b1e0ddffa
Create Date: 2023-03-30 15:26:17.807208

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'e41980d62bde'
down_revision = '4e6b1e0ddffa'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('defunct_pure_uuid_external_organisation',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_defunct_pure_uuid_external_organisation'))
    )
    op.create_table('defunct_pure_uuid_external_person',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_defunct_pure_uuid_external_person'))
    )
    op.create_table('defunct_pure_uuid_journal',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_defunct_pure_uuid_journal'))
    )
    op.create_table('defunct_pure_uuid_organisation',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_defunct_pure_uuid_organisation'))
    )
    op.create_table('defunct_pure_uuid_person',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_defunct_pure_uuid_person'))
    )
    op.create_table('defunct_pure_uuid_research_output',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_defunct_pure_uuid_research_output'))
    )

def downgrade():
    op.drop_table('defunct_pure_uuid_research_output')
    op.drop_table('defunct_pure_uuid_person')
    op.drop_table('defunct_pure_uuid_organisation')
    op.drop_table('defunct_pure_uuid_journal')
    op.drop_table('defunct_pure_uuid_external_person')
    op.drop_table('defunct_pure_uuid_external_organisation')
