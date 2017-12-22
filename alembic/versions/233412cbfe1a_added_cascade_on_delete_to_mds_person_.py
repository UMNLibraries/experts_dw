"""Added cascade on delete to mds_person_emplid FK.

Revision ID: 233412cbfe1a
Revises: cc093ad8dde6
Create Date: 2017-04-16 09:50:55.037702

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '233412cbfe1a'
down_revision = 'cc093ad8dde6'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_constraint('SYS_C00281377', 'mds_person_emplid', type_='foreignkey')
  op.create_foreign_key(
    None,
    'mds_person_emplid',
    'mds_person',
    ['uuid'],
    ['uuid'],
    ondelete='CASCADE'
  )

def downgrade():
  op.drop_constraint(None, 'mds_person_emplid', type_='foreignkey')
  op.create_foreign_key('SYS_C00281377', 'mds_person_emplid', 'mds_person', ['uuid'], ['uuid'])
