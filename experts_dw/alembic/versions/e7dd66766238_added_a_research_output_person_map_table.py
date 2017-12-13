"""Added a research_output_person_map table.

Revision ID: e7dd66766238
Revises: 5c9b1b5a1a78
Create Date: 2017-04-28 16:14:39.129137

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'e7dd66766238'
down_revision = '5c9b1b5a1a78'
branch_labels = None
depends_on = None

def upgrade():
  op.create_table(
    'research_output_person_map',
    sa.Column('research_output_uuid', sa.String(length=36), nullable=False),
    sa.Column('person_uuid', sa.String(length=36), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=True),
    sa.Column('person_ordinal', sa.Integer(), nullable=False),
    sa.Column('person_name', sa.String(length=255), nullable=False),
    sa.Column('person_role', sa.String(length=255), nullable=True),
    sa.Column('person_pure_internal', sa.String(length=1), nullable=True),
    sa.ForeignKeyConstraint(['person_uuid'], ['person.uuid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['research_output_uuid'], ['research_output.uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('research_output_uuid', 'person_uuid')
  )

def downgrade():
  op.drop_table('research_output_person_map')
