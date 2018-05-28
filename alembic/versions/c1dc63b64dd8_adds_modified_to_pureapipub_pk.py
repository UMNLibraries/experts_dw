"""Adds modified to PureApiPub pk.

Revision ID: c1dc63b64dd8
Revises: e1ff947af0c9
Create Date: 2018-05-28 14:58:59.433055

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'c1dc63b64dd8'
down_revision = 'e1ff947af0c9'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_constraint(
    'SYS_C00492426',
    'pure_api_pub',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00492426',
    'pure_api_pub',
    ['uuid','modified']
  )

def downgrade():
  op.drop_constraint(
    'SYS_C00492426',
    'pure_api_pub',
    type_='primary'
  )
  op.create_primary_key(
    'SYS_C00492426',
    'pure_api_pub',
    ['uuid']
  )
