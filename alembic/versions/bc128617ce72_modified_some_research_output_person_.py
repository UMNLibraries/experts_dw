"""Modified some research_output_person_map columns.

Revision ID: bc128617ce72
Revises: a0ee4912db65
Create Date: 2017-05-01 10:03:47.044619

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'bc128617ce72'
down_revision = 'a0ee4912db65'
branch_labels = None
depends_on = None

def upgrade():
  op.add_column('research_output_person_map', sa.Column('first_name', sa.String(length=100), nullable=True))
  op.add_column('research_output_person_map', sa.Column('last_name', sa.String(length=100), nullable=True))
  op.create_index(op.f('ix_research_output_person_map_emplid'), 'research_output_person_map', ['emplid'], unique=False)
  op.drop_column('research_output_person_map', 'person_name')

def downgrade():
  op.add_column('research_output_person_map', sa.Column('person_name', sa.VARCHAR(length=255), nullable=False))
  op.drop_index(op.f('ix_research_output_person_map_emplid'), table_name='research_output_person_map')
  op.drop_column('research_output_person_map', 'last_name')
  op.drop_column('research_output_person_map', 'first_name')
