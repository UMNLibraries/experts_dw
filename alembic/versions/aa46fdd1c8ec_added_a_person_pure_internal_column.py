"""Added a person.pure_internal column.

Revision ID: aa46fdd1c8ec
Revises: 058b6b239e02
Create Date: 2017-05-05 12:30:03.943808

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'aa46fdd1c8ec'
down_revision = '058b6b239e02'
branch_labels = None
depends_on = None

def upgrade():
  op.add_column('person', sa.Column('pure_internal', sa.String(length=1), nullable=True))

def downgrade():
  op.drop_column('person', 'pure_internal')
