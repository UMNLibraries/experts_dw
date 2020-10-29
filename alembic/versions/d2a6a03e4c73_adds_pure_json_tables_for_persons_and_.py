"""Adds pure_json* tables for persons and orgs

Revision ID: d2a6a03e4c73
Revises: 3b630e7ae521
Create Date: 2020-10-28 09:52:37.293184

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'd2a6a03e4c73'
down_revision = '3b630e7ae521'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_json_external_organisation_516',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_external_organisation_516_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_external_organisation_516'))
    )
    op.create_table('pure_json_external_organisation_516_staging',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_external_organisation_516_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_external_organisation_516_staging'))
    )
    op.create_table('pure_json_external_person_516',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_external_person_516_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_external_person_516'))
    )
    op.create_table('pure_json_external_person_516_staging',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_external_person_516_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_external_person_516_staging'))
    )
    op.create_table('pure_json_organisational_unit_516',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_organisational_unit_516_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_organisational_unit_516'))
    )
    op.create_table('pure_json_organisational_unit_516_staging',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_organisational_unit_516_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_organisational_unit_516_staging'))
    )
    op.create_table('pure_json_person_516',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_person_516_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_person_516'))
    )
    op.create_table('pure_json_person_516_staging',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('inserted', sa.DateTime(), nullable=False),
    sa.Column('json_document', sa.Text(), nullable=False),
    sa.Column('updated', sa.DateTime(), nullable=False),
    sa.Column('pure_created', sa.DateTime(), nullable=False),
    sa.Column('pure_modified', sa.DateTime(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name=op.f('ck_pure_json_person_516_staging_json_document')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_person_516_staging'))
    )

def downgrade():
    op.drop_table('pure_json_person_516_staging')
    op.drop_table('pure_json_person_516')
    op.drop_table('pure_json_organisational_unit_516_staging')
    op.drop_table('pure_json_organisational_unit_516')
    op.drop_table('pure_json_external_person_516_staging')
    op.drop_table('pure_json_external_person_516')
    op.drop_table('pure_json_external_organisation_516_staging')
    op.drop_table('pure_json_external_organisation_516')
