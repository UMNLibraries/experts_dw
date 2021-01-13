"""Drops pure_json_organisational_unit* tables.

Revision ID: 72588a2ddfbd
Revises: 506bd2c263ab
Create Date: 2020-11-11 12:30:06.221015

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '72588a2ddfbd'
down_revision = '506bd2c263ab'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint(
        'ck_pure_json_organisational_unit_516_staging_json_document',
        'pure_json_organisational_unit_516_staging'
    )
    op.drop_table('pure_json_organisational_unit_516_staging')
    op.drop_constraint(
        'ck_pure_json_organisational_unit_516_json_document',
        'pure_json_organisational_unit_516'
    )
    op.drop_table('pure_json_organisational_unit_516')


def downgrade():
    op.create_table('pure_json_organisational_unit_516',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_organisational_unit_516_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_organisational_unit_516')
    )
    op.create_table('pure_json_organisational_unit_516_staging',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('json_document', sa.CLOB(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.Column('pure_created', oracle.DATE(), nullable=False),
    sa.Column('pure_modified', oracle.DATE(), nullable=False),
    sa.CheckConstraint('json_document IS JSON', name='ck_pure_json_organisational_unit_516_staging_json_document'),
    sa.PrimaryKeyConstraint('uuid', name='pk_pure_json_organisational_unit_516_staging')
    )
