"""Made umn_person_pure_org.pure_org_uuid a FK to pure_org.

Revision ID: 2f90cbc51fc7
Revises: 85f1f3068080
Create Date: 2017-05-05 09:22:19.452836

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2f90cbc51fc7'
down_revision = '85f1f3068080'
branch_labels = None
depends_on = None

def upgrade():
  op.alter_column(
    'umn_person_pure_org',
    'pure_org_uuid',
    existing_type=sa.VARCHAR(length=36),
    nullable=False
  )
  op.create_foreign_key(
    None,
    'umn_person_pure_org',
    'pure_org',
    ['pure_org_uuid'],
    ['pure_uuid'],
    ondelete='CASCADE'
  )

def downgrade():
  # Would need the generated constraint name for this to work:
  op.drop_constraint(None, 'umn_person_pure_org', type_='foreignkey')
  op.alter_column(
    'umn_person_pure_org',
    'pure_org_uuid',
    existing_type=sa.VARCHAR(length=36),
    nullable=True
  )
