"""Made umn_person_pure_org.pure_org_uuid part of the PK.

Revision ID: 058b6b239e02
Revises: 2f90cbc51fc7
Create Date: 2017-05-05 09:29:22.569517

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '058b6b239e02'
down_revision = '2f90cbc51fc7'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_constraint('SYS_C00284282', 'umn_person_pure_org', type_='primary')
  op.alter_column(
    'umn_person_pure_org',
    'pure_org_id',
    existing_type=sa.VARCHAR(length=50),
    nullable=True
  )
  op.create_primary_key(
    'SYS_C00284282',
    'umn_person_pure_org',
    ['person_uuid','pure_org_uuid','job_description','start_date']
  )

def downgrade():
  op.drop_constraint('SYS_C00284282', 'umn_person_pure_org', type_='primary')
  op.alter_column(
    'umn_person_pure_org',
    'pure_org_id',
    existing_type=sa.VARCHAR(length=50),
    nullable=False
  )
  op.create_primary_key(
    'SYS_C00284282',
    'umn_person_pure_org',
    ['person_uuid','pure_org_id','job_description','start_date']
  )
