"""Removes now-unused umn_dept_pure_org column: umn_dept_id.

Revision ID: 7b8a16385f5a
Revises: e993e232a8c0
Create Date: 2018-10-15 18:02:32.028815

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '7b8a16385f5a'
down_revision = 'e993e232a8c0'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('umn_dept_pure_org', 'umn_dept_id')

def downgrade():
    op.add_column('umn_dept_pure_org', sa.Column('umn_dept_id', sa.INTEGER()))
