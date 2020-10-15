"""Renames 'json' column to 'record' in versioned pure_json_* tables.

Revision ID: d3168b930efb
Revises: 4af6a9d12f7c
Create Date: 2020-09-18 09:16:53.780553

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'd3168b930efb'
down_revision = '4af6a9d12f7c'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('pure_json_change_516', sa.Column('record', sa.Text(), nullable=False))
    op.create_check_constraint('record_json', 'pure_json_change_516', 'record IS JSON')
    op.drop_constraint('ck_pure_json_change_516_json', 'pure_json_change_516')
    op.drop_column('pure_json_change_516', 'json')

    op.add_column('pure_json_change_517', sa.Column('record', sa.Text(), nullable=False))
    op.create_check_constraint('record_json', 'pure_json_change_517', 'record IS JSON')
    op.drop_constraint('ck_pure_json_change_517_json', 'pure_json_change_517')
    op.drop_column('pure_json_change_517', 'json')

    op.add_column('pure_json_person_516', sa.Column('record', sa.Text(), nullable=False))
    op.create_check_constraint('record_json', 'pure_json_person_516', 'record IS JSON')
    op.drop_constraint('ck_pure_json_person_516_json', 'pure_json_person_516')
    op.drop_column('pure_json_person_516', 'json')

    op.add_column('pure_json_person_516_staging', sa.Column('record', sa.Text(), nullable=False))
    op.create_check_constraint('record_json', 'pure_json_person_516_staging', 'record IS JSON')
    op.drop_constraint('ck_pure_json_person_516_staging_json', 'pure_json_person_516_staging')
    op.drop_column('pure_json_person_516_staging', 'json')

    op.add_column('pure_json_person_517', sa.Column('record', sa.Text(), nullable=False))
    op.create_check_constraint('record_json', 'pure_json_person_517', 'record IS JSON')
    op.drop_constraint('ck_pure_json_person_517_json', 'pure_json_person_517')
    op.drop_column('pure_json_person_517', 'json')

    op.add_column('pure_json_person_517_staging', sa.Column('record', sa.Text(), nullable=False))
    op.create_check_constraint('record_json', 'pure_json_person_517_staging', 'record IS JSON')
    op.drop_constraint('ck_pure_json_person_517_staging_json', 'pure_json_person_517_staging')
    op.drop_column('pure_json_person_517_staging', 'json')

def downgrade():
    op.add_column('pure_json_person_517_staging', sa.Column('json', sa.CLOB(), nullable=False))
    op.create_check_constraint('json', 'pure_json_person_517_staging', 'JSON IS JSON')
    op.drop_constraint('ck_pure_json_person_517_staging_record_json', 'pure_json_person_517_staging')
    op.drop_column('pure_json_person_517_staging', 'record')

    op.add_column('pure_json_person_517', sa.Column('json', sa.CLOB(), nullable=False))
    op.create_check_constraint('json', 'pure_json_person_517', 'JSON IS JSON')
    op.drop_constraint('ck_pure_json_person_517_record_json', 'pure_json_person_517')
    op.drop_column('pure_json_person_517', 'record')

    op.add_column('pure_json_person_516_staging', sa.Column('json', sa.CLOB(), nullable=False))
    op.create_check_constraint('json', 'pure_json_person_516_staging', 'JSON IS JSON')
    op.drop_constraint('ck_pure_json_person_516_staging_record_json', 'pure_json_person_516_staging')
    op.drop_column('pure_json_person_516_staging', 'record')

    op.add_column('pure_json_person_516', sa.Column('json', sa.CLOB(), nullable=False))
    op.create_check_constraint('json', 'pure_json_person_516', 'JSON IS JSON')
    op.drop_constraint('ck_pure_json_person_516_record_json', 'pure_json_person_516')
    op.drop_column('pure_json_person_516', 'record')

    op.add_column('pure_json_change_517', sa.Column('json', sa.CLOB(), nullable=False))
    op.create_check_constraint('json', 'pure_json_change_517', 'JSON IS JSON')
    op.drop_constraint('ck_pure_json_change_517_record_json', 'pure_json_change_517')
    op.drop_column('pure_json_change_517', 'record')

    op.add_column('pure_json_change_516', sa.Column('json', sa.CLOB(), nullable=False))
    op.create_check_constraint('json', 'pure_json_change_516', 'JSON IS JSON')
    op.drop_constraint('ck_pure_json_change_516_record_json', 'pure_json_change_516')
    op.drop_column('pure_json_change_516', 'record')
