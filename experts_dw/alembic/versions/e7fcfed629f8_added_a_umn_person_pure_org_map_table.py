"""Added a umn_person_pure_org_map table.

Revision ID: e7fcfed629f8
Revises: 5ab0e80e545c
Create Date: 2017-04-21 13:37:53.230265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7fcfed629f8'
down_revision = '5ab0e80e545c'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    'umn_person_pure_org_map',
    sa.Column('person_uuid', sa.String(length=36), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('pure_org_id', sa.String(length=50), nullable=False),
    sa.Column('job_description', sa.String(length=255), nullable=True),
    sa.Column('employed_as', sa.String(length=50), nullable=True),
    sa.Column('staff_type', sa.String(length=11), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('primary', sa.String(length=1), nullable=True),
    sa.ForeignKeyConstraint(['person_uuid'], ['person.uuid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['pure_org_id'], ['pure_org.pure_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('emplid', 'pure_org_id')
  )
  op.create_index(op.f('ix_person_emplid'), 'person', ['emplid'], unique=False)
  op.create_index(op.f('ix_person_pure_id'), 'person', ['pure_id'], unique=False)
  op.create_index(op.f('ix_person_pure_uuid'), 'person', ['pure_uuid'], unique=False)

def downgrade():
  op.drop_index(op.f('ix_person_pure_uuid'), table_name='person')
  op.drop_index(op.f('ix_person_pure_id'), table_name='person')
  op.drop_index(op.f('ix_person_emplid'), table_name='person')
  op.drop_table('umn_person_pure_org_map')
