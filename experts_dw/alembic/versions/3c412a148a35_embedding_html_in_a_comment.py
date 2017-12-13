"""Embedding HTML in a comment.

Revision ID: 3c412a148a35
Revises: 8a1d246e57ec
Create Date: 2017-06-11 12:25:24.393167

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3c412a148a35'
down_revision = '8a1d246e57ec'
branch_labels = None
depends_on = None

def upgrade():
  op.execute("comment on column EXPERT.PUB.OWNER_PURE_ORG_UUID is 'Unique ID for the organization that owns the item in our <a href=\"https://experts.umn.edu/\">Elsevier Pure database</a>.'");

def downgrade():
  op.execute("comment on column EXPERT.PUB.OWNER_PURE_ORG_UUID is 'Unique ID for the organization that owns the item in our Elsevier Pure database (https://experts.umn.edu/).'");
