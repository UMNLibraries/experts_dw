"""Adds IS JSON column constraints to PURE_API_* tables

Revision ID: 36e9e9794287
Revises: 095d39509575
Create Date: 2020-04-07 15:57:28.632614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36e9e9794287'
down_revision = '3dca32d513ff'
branch_labels = None
depends_on = None


def upgrade():
    op.create_check_constraint('json', 'pure_api_pub', 'JSON IS JSON')
    op.create_check_constraint('json', 'pure_api_internal_person', 'JSON IS JSON')
    op.create_check_constraint('json', 'pure_api_external_person', 'JSON IS JSON')
    op.create_check_constraint('json', 'pure_api_internal_org', 'JSON IS JSON')
    op.create_check_constraint('json', 'pure_api_external_org', 'JSON IS JSON')


def downgrade():
    op.drop_constraint('ck_pure_api_pub_json', 'pure_api_pub')
    op.drop_constraint('ck_pure_api_internal_person_json', 'pure_api_internal_person')
    op.drop_constraint('ck_pure_api_external_person_json', 'pure_api_external_person')
    op.drop_constraint('ck_pure_api_internal_org_json', 'pure_api_internal_org')
    op.drop_constraint('ck_pure_api_external_org_json', 'pure_api_external_org')
