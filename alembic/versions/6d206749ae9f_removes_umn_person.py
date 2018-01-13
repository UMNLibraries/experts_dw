"""Removes umn_person.

Revision ID: 6d206749ae9f
Revises: 92e3be308009
Create Date: 2018-01-13 15:21:22.622353

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '6d206749ae9f'
down_revision = '92e3be308009'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('umn_person')

def downgrade():
    op.create_table('umn_person',
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('emplid', name='sys_c00383118')
    )
