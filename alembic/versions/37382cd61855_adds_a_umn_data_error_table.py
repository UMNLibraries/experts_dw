"""Adds a umn_data_error table.

Revision ID: 37382cd61855
Revises: 071a7e236cce
Create Date: 2019-02-28 16:10:15.676055

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '37382cd61855'
down_revision = '071a7e236cce'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('umn_data_error',
    sa.Column('error_id', sa.String(length=40), nullable=False),
    sa.Column('message', sa.String(length=255), nullable=False),
    sa.Column('jobcode', sa.String(length=13), nullable=True),
    sa.Column('deptid', sa.String(length=10), nullable=True),
    sa.Column('emplid', sa.String(length=11), nullable=True),
    sa.Column('first_seen', sa.DateTime(), nullable=False),
    sa.Column('last_seen', sa.DateTime(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.Column('notified', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('error_id')
    )

def downgrade():
    op.drop_table('umn_data_error')
