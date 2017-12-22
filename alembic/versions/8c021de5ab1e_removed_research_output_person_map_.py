"""Removed research_output_person_map.research_output_uuid.

Revision ID: 8c021de5ab1e
Revises: f9d0ad353c15
Create Date: 2017-05-05 13:08:29.269035

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8c021de5ab1e'
down_revision = 'f9d0ad353c15'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_constraint('SYS_C00287195', 'research_output_person_map', type_='primary')
  op.drop_constraint('SYS_C00287197', 'research_output_person_map', type_='foreignkey')
  op.drop_column('research_output_person_map', 'research_output_uuid')

def downgrade():
  op.add_column(
    'research_output_person_map',
    sa.Column('research_output_uuid', sa.VARCHAR(length=36), nullable=False)
  )
  op.create_foreign_key(
    'SYS_C00287197',
    'research_output_person_map',
    'research_output',
    ['research_output_uuid'],
    ['uuid'],
    ondelete='CASCADE'
  )
  op.create_primary_key(
    'SYS_C00287195',
    'research_output_person_map',
    ['research_output_uuid','person_uuid']
  )
