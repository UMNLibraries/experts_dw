"""Adds PersonScopusId, with a many-to-one relationship to Person.

Revision ID: 7c32ff151649
Revises: f4915a36781d
Create Date: 2018-05-01 15:29:29.018591

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '7c32ff151649'
down_revision = 'f4915a36781d'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    'person_scopus_id',
    sa.Column('person_uuid', sa.String(length=36), nullable=False),
    sa.Column('scopus_id', sa.String(length=35), nullable=False),
    sa.ForeignKeyConstraint(['person_uuid'], ['person.uuid'], ),
    sa.PrimaryKeyConstraint('person_uuid', 'scopus_id')
  )

def downgrade():
  op.drop_table('person_scopus_id')
