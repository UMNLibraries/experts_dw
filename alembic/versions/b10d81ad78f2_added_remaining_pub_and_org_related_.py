"""Added remaining pub- and org-related tables.

Revision ID: b10d81ad78f2
Revises: 551c23438c97
Create Date: 2017-05-08 14:42:05.997541

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b10d81ad78f2'
down_revision = '551c23438c97'
branch_labels = None
depends_on = None

def upgrade():
  op.create_table('person_pure_org',
    sa.Column('person_uuid', sa.String(length=36), nullable=False),
    sa.Column('pure_org_uuid', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['person_uuid'], ['person.uuid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['pure_org_uuid'], ['pure_org.pure_uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('person_uuid', 'pure_org_uuid')
  )
  op.create_table('pub_person_pure_org',
    sa.Column('pub_uuid', sa.String(length=36), nullable=False),
    sa.Column('person_uuid', sa.String(length=36), nullable=False),
    sa.Column('pure_org_uuid', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['person_uuid'], ['person.uuid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['pub_uuid'], ['pub.uuid'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['pure_org_uuid'], ['pure_org.pure_uuid'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('pub_uuid', 'person_uuid', 'pure_org_uuid')
  )

def downgrade():
  op.drop_table('pub_person_pure_org')
  op.drop_table('person_pure_org')
