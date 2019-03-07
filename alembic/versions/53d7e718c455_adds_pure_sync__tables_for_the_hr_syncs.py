"""Adds pure_sync_* tables for the HR syncs.

Revision ID: 53d7e718c455
Revises: 37382cd61855
Create Date: 2019-03-07 15:02:09.973879

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '53d7e718c455'
down_revision = '37382cd61855'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_sync_person_data',
    sa.Column('person_id', sa.String(length=1024), nullable=False),
    sa.Column('first_name', sa.String(length=1024), nullable=True),
    sa.Column('last_name', sa.String(length=1024), nullable=False),
    sa.Column('visibility', sa.String(length=1024), nullable=False),
    sa.Column('profiled', sa.Boolean(), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('internet_id', sa.String(length=15), nullable=True),
    sa.Column('postnominal', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('person_id')
    )
    op.create_table('pure_sync_staff_org_association',
    sa.Column('staff_org_association_id', sa.String(length=1024), nullable=False),
    sa.Column('person_id', sa.String(length=1024), nullable=False),
    sa.Column('period_start_date', sa.DateTime(), nullable=False),
    sa.Column('period_end_date', sa.DateTime(), nullable=True),
    sa.Column('org_id', sa.String(length=1024), nullable=False),
    sa.Column('employment_type', sa.String(length=1024), nullable=False),
    sa.Column('staff_type', sa.String(length=1024), nullable=False),
    sa.Column('visibility', sa.String(length=1024), nullable=False),
    sa.Column('primary_association', sa.Boolean(), nullable=False),
    sa.Column('job_description', sa.String(length=1024), nullable=False),
    sa.ForeignKeyConstraint(['person_id'], ['pure_sync_person_data.person_id'], ),
    sa.PrimaryKeyConstraint('staff_org_association_id')
    )
    op.create_table('pure_sync_user_data',
    sa.Column('person_id', sa.String(length=1024), nullable=False),
    sa.Column('first_name', sa.String(length=1024), nullable=True),
    sa.Column('last_name', sa.String(length=1024), nullable=True),
    sa.Column('user_name', sa.String(length=1024), nullable=False),
    sa.Column('email', sa.String(length=1024), nullable=False),
    sa.ForeignKeyConstraint(['person_id'], ['pure_sync_person_data.person_id'], ),
    sa.PrimaryKeyConstraint('person_id')
    )

def downgrade():
    op.drop_table('pure_sync_user_data')
    op.drop_table('pure_sync_staff_org_association')
    op.drop_table('pure_sync_person_data')
