"""Added pub FK back in to pub_person.

Revision ID: 7f24240aabd0
Revises: 6d594384b371
Create Date: 2017-05-06 09:33:30.044973

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f24240aabd0'
down_revision = '6d594384b371'
branch_labels = None
depends_on = None


def upgrade():
  op.add_column('pub_person', sa.Column('pub_uuid', sa.String(length=36), nullable=False))
  op.create_foreign_key(None, 'pub_person', 'pub', ['pub_uuid'], ['uuid'], ondelete='CASCADE')
  op.create_primary_key(None, 'pub_person', ['pub_uuid','person_uuid'])
  op.drop_index('ix_rsrch_output_persom_emplid', table_name='pub_person')

def downgrade():
  # Would need to get the generated constraint names for this to work:
  op.drop_constraint(None, 'pub_person', type_='primary')
  op.drop_constraint(None, 'pub_person', type_='foreignkey')
  op.drop_column('pub_person', 'pub_uuid')
  op.create_index('ix_rsrch_output_persom_emplid', 'pub_person', ['emplid'], unique=False)
