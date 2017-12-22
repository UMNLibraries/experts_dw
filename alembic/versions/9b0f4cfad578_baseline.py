"""baseline

Revision ID: 9b0f4cfad578
Revises: 
Create Date: 2017-02-13 15:51:32.863208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b0f4cfad578'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    'person',
    sa.Column('emplid', sa.String(11), primary_key=True),
    sa.Column('timestamp', sa.DateTime(), default=sa.func.current_timestamp())
  )

def downgrade():
  op.drop_table('person')
