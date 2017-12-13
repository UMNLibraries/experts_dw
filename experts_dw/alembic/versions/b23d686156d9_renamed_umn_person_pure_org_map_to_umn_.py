"""Renamed umn_person_pure_org_map to umn_person_pure_org.

Revision ID: b23d686156d9
Revises: b54c5e753921
Create Date: 2017-05-05 09:03:56.850747

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'b23d686156d9'
down_revision = 'b54c5e753921'
branch_labels = None
depends_on = None

def upgrade():
   op.rename_table('umn_person_pure_org_map', 'umn_person_pure_org')

def downgrade():
   op.rename_table('umn_person_pure_org', 'umn_person_pure_org_map')
