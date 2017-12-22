"""Removed emplid FK from mds_person_internet_id.

Revision ID: d62895e358d3
Revises: 4111a5f6f775
Create Date: 2017-04-15 11:44:42.404059

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd62895e358d3'
down_revision = '4111a5f6f775'
branch_labels = None
depends_on = None


def upgrade():
  op.drop_constraint('SYS_C00281671', 'mds_person_internet_id', type_='foreignkey')

def downgrade():
  op.create_foreign_key('SYS_C00281671', 'mds_person_internet_id', 'mds_person_emplid', ['emplid'], ['emplid'], ondelete='CASCADE')
