"""Added a person table.

Revision ID: 5ab0e80e545c
Revises: 761117a54535
Create Date: 2017-04-18 14:59:24.791510

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5ab0e80e545c'
down_revision = '761117a54535'
branch_labels = None
depends_on = None

def upgrade():
  op.create_table(
    'person',
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('pure_uuid', sa.String(length=36), nullable=True),
    sa.Column('pure_id', sa.String(length=11), nullable=True),
    sa.Column('orcid', sa.String(length=20), nullable=True),
    sa.Column('scopus_id', sa.String(length=35), nullable=True),
    sa.Column('hindex', sa.Integer(), nullable=True),
    sa.Column('emplid', sa.String(length=11), nullable=True),
    sa.Column('internet_id', sa.String(length=15), nullable=True),
    sa.Column('first_name', sa.String(length=100), nullable=True),
    sa.Column('last_name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('uuid')
  )
  op.alter_column(
    'mds_person_first_name',
    'first_name',
    existing_type=sa.VARCHAR(length=30),
    type_=sa.String(length=100),
    existing_nullable=True
  )
  op.alter_column(
    'mds_person_last_name',
    'last_name',
    existing_type=sa.VARCHAR(length=30),
    type_=sa.String(length=100),
    existing_nullable=True
  )
  op.alter_column(
    'mds_person_middle_name',
    'middle_name',
    existing_type=sa.VARCHAR(length=30),
    type_=sa.String(length=100),
    existing_nullable=True
  )
  op.alter_column(
    'mds_person_name_suffix',
    'name_suffix',
    existing_type=sa.VARCHAR(length=15),
    type_=sa.String(length=30),
    existing_nullable=True
  )
  op.alter_column(
    'mds_person_preferred_name',
    'preferred_name',
    existing_type=sa.VARCHAR(length=50),
    type_=sa.String(length=255),
    existing_nullable=True
  )

def downgrade():
  op.alter_column(
    'mds_person_preferred_name',
    'preferred_name',
    existing_type=sa.String(length=255),
    type_=sa.VARCHAR(length=50),
    existing_nullable=True
  )
  op.alter_column(
    'mds_person_name_suffix',
    'name_suffix',
    existing_type=sa.String(length=30),
    type_=sa.VARCHAR(length=15),
    existing_nullable=True
  )
  op.alter_column(
    'mds_person_middle_name',
    'middle_name',
    existing_type=sa.String(length=100),
    type_=sa.VARCHAR(length=30),
    existing_nullable=True
  )
  op.alter_column(
    'mds_person_last_name',
    'last_name',
    existing_type=sa.String(length=100),
    type_=sa.VARCHAR(length=30),
    existing_nullable=True
  )
  op.alter_column(
    'mds_person_first_name',
    'first_name',
    existing_type=sa.String(length=100),
    type_=sa.VARCHAR(length=30),
    existing_nullable=True
  )
  op.drop_table('person')
