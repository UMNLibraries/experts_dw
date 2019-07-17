"""Adds columns to umn_data_error for better reporting.

Revision ID: 58f9c020e85b
Revises: 7fc7625a8065
Create Date: 2019-07-17 14:43:02.534157

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '58f9c020e85b'
down_revision = '7fc7625a8065'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('umn_data_error', sa.Column('deptid_descr', sa.String(length=30), nullable=True))
    op.add_column('umn_data_error', sa.Column('persons_in_dept', sa.Integer(), nullable=True))
    op.add_column('umn_data_error', sa.Column('um_campus', sa.String(length=10), nullable=True))
    op.add_column('umn_data_error', sa.Column('um_campus_descr', sa.String(length=30), nullable=True))
    op.add_column('umn_data_error', sa.Column('um_college', sa.String(length=10), nullable=True))
    op.add_column('umn_data_error', sa.Column('um_college_descr', sa.String(length=30), nullable=True))

def downgrade():
    op.drop_column('umn_data_error', 'um_college_descr')
    op.drop_column('umn_data_error', 'um_college')
    op.drop_column('umn_data_error', 'um_campus_descr')
    op.drop_column('umn_data_error', 'um_campus')
    op.drop_column('umn_data_error', 'persons_in_dept')
    op.drop_column('umn_data_error', 'deptid_descr')
