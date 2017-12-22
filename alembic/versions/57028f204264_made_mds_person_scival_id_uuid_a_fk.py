"""Made mds_person_scival_id.uuid a FK.

Revision ID: 57028f204264
Revises: a3a61add7f31
Create Date: 2017-04-13 20:37:39.261520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57028f204264'
down_revision = 'a3a61add7f31'
branch_labels = None
depends_on = None


def upgrade():
  op.alter_column(
    'mds_person_scival_id',
    'uuid',
    existing_type=sa.VARCHAR(length=36),
    nullable=False
  )
  op.create_foreign_key(None, 'mds_person_scival_id', 'mds_person', ['uuid'], ['uuid'])


def downgrade():
  op.drop_constraint(None, 'mds_person_scival_id', type_='foreignkey')
  op.alter_column(
    'mds_person_scival_id',
    'uuid',
    existing_type=sa.VARCHAR(length=36),
    nullable=True
  )
