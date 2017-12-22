"""Added a umn_dept_pure_org_map table.

Revision ID: a4864a963f7f
Revises: 3fb5e65aa3de
Create Date: 2017-04-17 15:47:52.158372

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a4864a963f7f'
down_revision = '3fb5e65aa3de'
branch_labels = None
depends_on = None

def upgrade():
  op.create_table(
    'umn_dept_pure_org_map',
    sa.Column('umn_id', sa.Integer(), nullable=False),
    sa.Column('umn_name', sa.String(length=255), nullable=True),
    sa.Column('pure_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pure_id'], ['pure_org.id'], ),
    sa.PrimaryKeyConstraint('umn_id')
  )

def downgrade():
  op.drop_table('umn_dept_pure_org_map')
