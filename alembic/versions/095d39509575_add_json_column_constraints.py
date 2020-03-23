"""add json column constraints

Revision ID: 095d39509575
Revises: 5df53f647a97
Create Date: 2020-03-23 09:20:53.888738

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '095d39509575'
down_revision = '5df53f647a97'
branch_labels = None
depends_on = None


def upgrade():
    op.create_check_constraint('ck_pure_json_organisation_json', 'pure_json_organisation', 'JSON IS JSON')
    op.create_check_constraint('ck_pure_json_person_json', 'pure_json_person', 'JSON IS JSON')
    op.create_check_constraint('ck_pure_json_research_output_json', 'pure_json_research_output', 'JSON IS JSON')


def downgrade():
    op.drop_constraint('ck_pure_json_organisation_json')
    op.drop_constraint('ck_pure_json_person_json')
    op.drop_constraint('ck_pure_json_research_output_json')
