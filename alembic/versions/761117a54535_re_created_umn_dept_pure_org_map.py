"""Re-created umn_dept_pure_org_map.

Revision ID: 761117a54535
Revises: fe7a8f156b37
Create Date: 2017-04-18 10:21:33.959260

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '761117a54535'
down_revision = 'fe7a8f156b37'
branch_labels = None
depends_on = None

def upgrade():
  op.create_table(
    'umn_dept_pure_org_map',
    sa.Column('umn_dept_id', sa.Integer(), nullable=False),
    sa.Column('umn_dept_name', sa.String(length=255), nullable=True),
    sa.Column('pure_org_id', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['pure_org_id'], ['pure_org.pure_id'], ),
    sa.PrimaryKeyConstraint('umn_dept_id')
  )

def downgrade():
  op.drop_table('umn_dept_pure_org_map')
