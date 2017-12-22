"""Added umn_person_pure_org_map.start_date to the PK.

Revision ID: 7555936f7b6c
Revises: 1df9620bad69
Create Date: 2017-04-21 15:24:23.592126

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '7555936f7b6c'
down_revision = '1df9620bad69'
branch_labels = None
depends_on = None

def upgrade():
  op.add_column(
    'umn_person_pure_org_map',
    sa.Column('pure_person_id', sa.String(length=11),
    nullable=False)
  )
  # Changed PK manually, because alembic doesn't seem able to do it.

def downgrade():
  op.drop_column('umn_person_pure_org_map', 'pure_person_id')
  # Would have to PK manually, because alembic doesn't seem able to do it.
