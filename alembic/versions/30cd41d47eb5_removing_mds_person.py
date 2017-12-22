"""Removing mds_person.

Revision ID: 30cd41d47eb5
Revises: 2073258b3a22
Create Date: 2017-04-13 16:18:59.849948

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '30cd41d47eb5'
down_revision = '2073258b3a22'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_table('mds_person')

def downgrade():
  op.create_table(
    'mds_person',
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('emplid', name='sys_c00264293')
  )
