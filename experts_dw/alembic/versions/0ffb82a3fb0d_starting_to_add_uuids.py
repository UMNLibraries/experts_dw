"""Starting to add uuids.

Revision ID: 0ffb82a3fb0d
Revises: 30cd41d47eb5
Create Date: 2017-04-13 16:54:02.813062

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ffb82a3fb0d'
down_revision = '30cd41d47eb5'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('mds_person',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('uuid')
  )
  op.add_column('mds_person_emplid', sa.Column('uuid', sa.String(length=36), nullable=True))


def downgrade():
  op.drop_column('mds_person_emplid', 'uuid')
  op.drop_table('mds_person')
