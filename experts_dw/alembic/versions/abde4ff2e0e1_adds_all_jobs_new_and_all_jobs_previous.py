"""Adds all_jobs_new and all_jobs_previous.

Revision ID: abde4ff2e0e1
Revises: e640c0411156
Create Date: 2017-12-15 16:44:40.153603

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'abde4ff2e0e1'
down_revision = 'e640c0411156'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table('all_jobs_new',
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('jobcode', sa.String(length=6), nullable=False),
    sa.Column('jobcode_descr', sa.String(length=35), nullable=True),
    sa.Column('job_indicator', sa.String(length=40), nullable=True),
    sa.Column('empl_rcdno', sa.String(length=4), nullable=True),
    sa.Column('paygroup', sa.String(length=12), nullable=True),
    sa.Column('deptid', sa.String(length=10), nullable=False),
    sa.Column('deptid_descr', sa.String(length=30), nullable=True),
    sa.Column('um_jobcode_group', sa.String(length=8), nullable=True),
    sa.Column('um_college', sa.String(length=20), nullable=True),
    sa.Column('um_college_descr', sa.String(length=30), nullable=True),
    sa.Column('campus', sa.String(length=20), nullable=True),
    sa.Column('um_zdeptid', sa.String(length=80), nullable=True),
    sa.Column('um_zdeptid_descr', sa.String(length=30), nullable=True),
    sa.Column('status_flg', sa.String(length=1), nullable=True),
    sa.Column('record_source', sa.String(length=1), nullable=True),
    sa.Column('job_entry_dt', sa.DateTime(), nullable=True),
    sa.Column('position_entry_dt', sa.DateTime(), nullable=True),
    sa.Column('calculated_start_dt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('emplid', 'jobcode', 'deptid')
  )
  op.create_table('all_jobs_previous',
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('jobcode', sa.String(length=6), nullable=False),
    sa.Column('jobcode_descr', sa.String(length=35), nullable=True),
    sa.Column('job_indicator', sa.String(length=40), nullable=True),
    sa.Column('empl_rcdno', sa.String(length=4), nullable=True),
    sa.Column('paygroup', sa.String(length=12), nullable=True),
    sa.Column('deptid', sa.String(length=10), nullable=False),
    sa.Column('deptid_descr', sa.String(length=30), nullable=True),
    sa.Column('um_jobcode_group', sa.String(length=8), nullable=True),
    sa.Column('um_college', sa.String(length=20), nullable=True),
    sa.Column('um_college_descr', sa.String(length=30), nullable=True),
    sa.Column('campus', sa.String(length=20), nullable=True),
    sa.Column('um_zdeptid', sa.String(length=80), nullable=True),
    sa.Column('um_zdeptid_descr', sa.String(length=30), nullable=True),
    sa.Column('status_flg', sa.String(length=1), nullable=True),
    sa.Column('record_source', sa.String(length=1), nullable=True),
    sa.Column('job_entry_dt', sa.DateTime(), nullable=True),
    sa.Column('position_entry_dt', sa.DateTime(), nullable=True),
    sa.Column('calculated_start_dt', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('emplid', 'jobcode', 'deptid')
  )


def downgrade():
  op.drop_table('all_jobs_previous')
  op.drop_table('all_jobs_new')
