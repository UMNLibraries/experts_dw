"""Added an mpds_person_emplid table.

Revision ID: 85d25911adf2
Revises: 225a5061088c
Create Date: 2017-04-13 15:00:34.994073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85d25911adf2'
down_revision = '225a5061088c'
branch_labels = None
depends_on = None

def upgrade():
  op.create_table(
    'mds_person_emplid',
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('emplid')
  )


def downgrade():
  op.drop_table('mds_person_emplid')
