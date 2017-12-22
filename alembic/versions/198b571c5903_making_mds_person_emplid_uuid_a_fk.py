"""Making mds_person_emplid.uuid a FK.

Revision ID: 198b571c5903
Revises: 0ffb82a3fb0d
Create Date: 2017-04-13 17:09:50.029223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '198b571c5903'
down_revision = '0ffb82a3fb0d'
branch_labels = None
depends_on = None

def upgrade():
  op.alter_column(
    'mds_person_emplid',
    'uuid',
    existing_type=sa.VARCHAR(length=36),
    nullable=False
  )
  op.create_foreign_key(None, 'mds_person_emplid', 'mds_person', ['uuid'], ['uuid'])


def downgrade():
  op.drop_constraint(None, 'mds_person_emplid', type_='foreignkey')
  op.alter_column(
    'mds_person_emplid',
    'uuid',
    existing_type=sa.VARCHAR(length=36),
    nullable=True
  )
