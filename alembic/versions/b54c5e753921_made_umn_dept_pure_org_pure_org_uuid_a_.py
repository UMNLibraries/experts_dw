"""Made umn_dept_pure_org.pure_org_uuid a FK to pure_org.

Revision ID: b54c5e753921
Revises: 495667f4ed9b
Create Date: 2017-05-05 08:32:13.913685

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'b54c5e753921'
down_revision = '495667f4ed9b'
branch_labels = None
depends_on = None

def upgrade():
  op.alter_column(
    'umn_dept_pure_org',
    'pure_org_uuid',
    existing_type=sa.VARCHAR(length=36),
    nullable=False
  )
  op.create_foreign_key(
    None,
    'umn_dept_pure_org',
    'pure_org',
    ['pure_org_uuid'],
    ['pure_uuid'],
    ondelete='CASCADE'
  )

def downgrade():
  # Would need the generated constraint name for this to work:
  op.drop_constraint(None, 'umn_dept_pure_org', type_='foreignkey')
  op.alter_column(
    'umn_dept_pure_org',
    'pure_org_uuid',
    existing_type=sa.VARCHAR(length=36),
    nullable=True
  )
