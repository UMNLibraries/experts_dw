"""Adds some new pure_json_* tables with support for multiple versions.

Revision ID: 4af6a9d12f7c
Revises: 36e9e9794287
Create Date: 2020-09-11 13:10:22.972837

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '4af6a9d12f7c'
down_revision = '36e9e9794287'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_json_change_516',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=False),
    sa.Column('json', sa.Text(), nullable=False),
    sa.CheckConstraint('json IS JSON', name=op.f('ck_pure_json_change_516_json')),
    sa.PrimaryKeyConstraint('uuid', 'version', name=op.f('pk_pure_json_change_516'))
    )
    op.create_table('pure_json_change_516_history',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=False),
    sa.Column('processed', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'version', name=op.f('pk_pure_json_change_516_history'))
    )
    op.create_table('pure_json_change_517',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=False),
    sa.Column('json', sa.Text(), nullable=False),
    sa.CheckConstraint('json IS JSON', name=op.f('ck_pure_json_change_517_json')),
    sa.PrimaryKeyConstraint('uuid', 'version', name=op.f('pk_pure_json_change_517'))
    )
    op.create_table('pure_json_change_517_history',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('family_system_name', sa.String(length=150), nullable=False),
    sa.Column('change_type', sa.String(length=10), nullable=False),
    sa.Column('version', sa.Integer(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=False),
    sa.Column('processed', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', 'version', name=op.f('pk_pure_json_change_517_history'))
    )
    op.create_table('pure_json_person_516',
    sa.Column('json', sa.Text(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=True),
    sa.CheckConstraint('json IS JSON', name=op.f('ck_pure_json_person_516_json')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_person_516'))
    )
    op.create_table('pure_json_person_516_staging',
    sa.Column('json', sa.Text(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=True),
    sa.CheckConstraint('json IS JSON', name=op.f('ck_pure_json_person_516_staging_json')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_person_516_staging'))
    )
    op.create_table('pure_json_person_517',
    sa.Column('json', sa.Text(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=True),
    sa.CheckConstraint('json IS JSON', name=op.f('ck_pure_json_person_517_json')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_person_517'))
    )
    op.create_table('pure_json_person_517_staging',
    sa.Column('json', sa.Text(), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('modified', sa.DateTime(), nullable=False),
    sa.Column('downloaded', sa.DateTime(), nullable=True),
    sa.CheckConstraint('json IS JSON', name=op.f('ck_pure_json_person_517_staging_json')),
    sa.PrimaryKeyConstraint('uuid', name=op.f('pk_pure_json_person_517_staging'))
    )

def downgrade():
    op.drop_table('pure_json_person_517_staging')
    op.drop_table('pure_json_person_517')
    op.drop_table('pure_json_person_516_staging')
    op.drop_table('pure_json_person_516')
    op.drop_table('pure_json_change_517_history')
    op.drop_table('pure_json_change_517')
    op.drop_table('pure_json_change_516_history')
    op.drop_table('pure_json_change_516')
