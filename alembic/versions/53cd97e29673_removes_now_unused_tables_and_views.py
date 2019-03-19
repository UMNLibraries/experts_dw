"""Removes now-unused tables and views.

Revision ID: 53cd97e29673
Revises: 7d50429f27a7
Create Date: 2019-03-19 13:24:59.177381

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '53cd97e29673'
down_revision = '7d50429f27a7'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('pure_eligible_aff_job_chng_hst')
    op.drop_table('pure_eligible_emp_job_new')
    op.drop_table('pure_new_staff_dept_defaults')
    op.drop_table('umn_dept')
    op.drop_table('all_jobs_previous')
    op.drop_table('pure_eligible_aff_job_new')
    op.drop_table('affiliate_departments')
    op.drop_table('job_codes')
    op.drop_table('pure_eligible_emp_job_chng_hst')
    op.drop_table('pure_new_staff_pos_defaults')
    op.drop_table('all_jobs_new')

def downgrade():
    op.create_table('all_jobs_new',
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('jobcode', sa.VARCHAR(length=13), nullable=False),
    sa.Column('jobcode_descr', sa.VARCHAR(length=35), nullable=True),
    sa.Column('job_indicator', sa.VARCHAR(length=40), nullable=False),
    sa.Column('empl_rcdno', sa.VARCHAR(length=40), nullable=True),
    sa.Column('paygroup', sa.VARCHAR(length=12), nullable=True),
    sa.Column('deptid', sa.VARCHAR(length=10), nullable=False),
    sa.Column('deptid_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('um_jobcode_group', sa.VARCHAR(length=8), nullable=True),
    sa.Column('um_college', sa.VARCHAR(length=20), nullable=True),
    sa.Column('um_college_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('campus', sa.VARCHAR(length=20), nullable=True),
    sa.Column('um_zdeptid', sa.VARCHAR(length=80), nullable=True),
    sa.Column('um_zdeptid_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('status_flg', sa.VARCHAR(length=1), nullable=True),
    sa.Column('record_source', sa.VARCHAR(length=1), nullable=True),
    sa.Column('job_entry_dt', oracle.DATE(), nullable=True),
    sa.Column('position_entry_dt', oracle.DATE(), nullable=True),
    sa.Column('calculated_start_dt', oracle.DATE(), nullable=True),
    sa.Column('empl_status', sa.VARCHAR(length=4), nullable=True),
    sa.PrimaryKeyConstraint('emplid', 'jobcode', 'job_indicator', 'deptid', name='sys_c00384862')
    )
    op.create_table('pure_new_staff_pos_defaults',
    sa.Column('jobcode', sa.VARCHAR(length=13), nullable=False),
    sa.Column('jobcode_descr', sa.VARCHAR(length=35), nullable=True),
    sa.Column('um_jobcode_group', sa.VARCHAR(length=8), nullable=True),
    sa.Column('um_jobcode_group_descr', sa.VARCHAR(length=50), nullable=True),
    sa.Column('default_staff_type', sa.VARCHAR(length=11), nullable=False),
    sa.Column('default_employed_as', sa.VARCHAR(length=50), nullable=False),
    sa.PrimaryKeyConstraint('jobcode', name='sys_c00133949')
    )
    op.create_table('pure_eligible_emp_job_chng_hst',
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('empl_rcdno', sa.VARCHAR(length=40), nullable=True),
    sa.Column('effdt', oracle.DATE(), nullable=True),
    sa.Column('name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('jobcode', sa.VARCHAR(length=13), nullable=True),
    sa.Column('jobcode_descr', sa.VARCHAR(length=35), nullable=True),
    sa.Column('job_indicator', sa.VARCHAR(length=40), nullable=True),
    sa.Column('empl_status', sa.VARCHAR(length=4), nullable=True),
    sa.Column('paygroup', sa.VARCHAR(length=12), nullable=True),
    sa.Column('deptid', sa.VARCHAR(length=10), nullable=True),
    sa.Column('deptid_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('um_jobcode_group', sa.VARCHAR(length=8), nullable=True),
    sa.Column('um_college', sa.VARCHAR(length=20), nullable=True),
    sa.Column('um_college_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('um_zdeptid', sa.VARCHAR(length=80), nullable=True),
    sa.Column('um_zdeptid_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('status_flg', sa.VARCHAR(length=1), nullable=True),
    sa.Column('job_terminated', sa.VARCHAR(length=1), nullable=True),
    sa.Column('last_date_worked', oracle.DATE(), nullable=True),
    sa.Column('job_entry_dt', oracle.DATE(), nullable=True),
    sa.Column('position_entry_dt', oracle.DATE(), nullable=True),
    sa.Column('effseq', sa.INTEGER(), nullable=True),
    sa.Column('position_nbr', sa.VARCHAR(length=8), nullable=True),
    sa.Column('rrc', sa.VARCHAR(length=20), nullable=True),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('emplid', 'timestamp', name='sys_c00387279')
    )
    op.create_table('job_codes',
    sa.Column('id', oracle.NUMBER(precision=38, scale=0, asdecimal=False), nullable=False),
    sa.Column('jobcode', sa.VARCHAR(length=255), nullable=True),
    sa.Column('pool', sa.VARCHAR(length=255), nullable=True),
    sa.Column('descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('created_at', oracle.DATE(), nullable=False),
    sa.Column('updated_at', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('id', name='sys_c00131857')
    )
    op.create_table('affiliate_departments',
    sa.Column('id', oracle.NUMBER(precision=38, scale=0, asdecimal=False), nullable=False),
    sa.Column('deptid', sa.VARCHAR(length=255), nullable=True),
    sa.Column('descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('created_at', oracle.DATE(), nullable=False),
    sa.Column('updated_at', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('id', name='sys_c00131778')
    )
    op.create_table('pure_eligible_aff_job_new',
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('um_affiliate_id', sa.VARCHAR(length=2), nullable=False),
    sa.Column('effdt', oracle.DATE(), nullable=False),
    sa.Column('um_affil_relation', sa.VARCHAR(length=6), nullable=True),
    sa.Column('title', sa.VARCHAR(length=35), nullable=True),
    sa.Column('deptid', sa.VARCHAR(length=10), nullable=False),
    sa.Column('deptid_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('status', sa.VARCHAR(length=1), nullable=True),
    sa.Column('um_college', sa.VARCHAR(length=20), nullable=True),
    sa.Column('um_college_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('um_campus', sa.VARCHAR(length=20), nullable=True),
    sa.Column('um_zdeptid', sa.VARCHAR(length=80), nullable=True),
    sa.Column('um_zdeptid_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('status_flg', sa.VARCHAR(length=1), nullable=True),
    sa.PrimaryKeyConstraint('emplid', 'um_affiliate_id', 'effdt', 'deptid', name='sys_c00134504')
    )
    op.create_table('all_jobs_previous',
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('jobcode', sa.VARCHAR(length=13), nullable=False),
    sa.Column('jobcode_descr', sa.VARCHAR(length=35), nullable=True),
    sa.Column('job_indicator', sa.VARCHAR(length=40), nullable=False),
    sa.Column('empl_rcdno', sa.VARCHAR(length=40), nullable=True),
    sa.Column('paygroup', sa.VARCHAR(length=12), nullable=True),
    sa.Column('deptid', sa.VARCHAR(length=10), nullable=False),
    sa.Column('deptid_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('um_jobcode_group', sa.VARCHAR(length=8), nullable=True),
    sa.Column('um_college', sa.VARCHAR(length=20), nullable=True),
    sa.Column('um_college_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('campus', sa.VARCHAR(length=20), nullable=True),
    sa.Column('um_zdeptid', sa.VARCHAR(length=80), nullable=True),
    sa.Column('um_zdeptid_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('status_flg', sa.VARCHAR(length=1), nullable=True),
    sa.Column('record_source', sa.VARCHAR(length=1), nullable=True),
    sa.Column('job_entry_dt', oracle.DATE(), nullable=True),
    sa.Column('position_entry_dt', oracle.DATE(), nullable=True),
    sa.Column('calculated_start_dt', oracle.DATE(), nullable=True),
    sa.Column('empl_status', sa.VARCHAR(length=4), nullable=True),
    sa.PrimaryKeyConstraint('emplid', 'jobcode', 'job_indicator', 'deptid', name='sys_c00384866')
    )
    op.create_table('umn_dept',
    sa.Column('deptid', sa.INTEGER(), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('deptid', name='sys_c00383727')
    )
    op.create_table('pure_new_staff_dept_defaults',
    sa.Column('deptid', sa.VARCHAR(length=10), nullable=False),
    sa.Column('deptid_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('pure_org_id', sa.VARCHAR(length=50), nullable=True),
    sa.Column('jobcode', sa.VARCHAR(length=13), nullable=False),
    sa.Column('jobcode_descr', sa.VARCHAR(length=35), nullable=False),
    sa.Column('um_college', sa.VARCHAR(length=20), nullable=True),
    sa.Column('um_college_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('default_visibility', sa.VARCHAR(length=10), nullable=False),
    sa.Column('default_profiled', sa.VARCHAR(length=5), nullable=False),
    sa.PrimaryKeyConstraint('deptid', 'jobcode', 'jobcode_descr', name='sys_c00394480')
    )
    op.create_table('pure_eligible_emp_job_new',
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('empl_rcdno', sa.VARCHAR(length=40), nullable=False),
    sa.Column('effdt', oracle.DATE(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('jobcode', sa.VARCHAR(length=13), nullable=False),
    sa.Column('jobcode_descr', sa.VARCHAR(length=35), nullable=True),
    sa.Column('job_indicator', sa.VARCHAR(length=40), nullable=True),
    sa.Column('empl_status', sa.VARCHAR(length=4), nullable=False),
    sa.Column('paygroup', sa.VARCHAR(length=12), nullable=True),
    sa.Column('deptid', sa.VARCHAR(length=10), nullable=False),
    sa.Column('deptid_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('um_jobcode_group', sa.VARCHAR(length=8), nullable=True),
    sa.Column('um_college', sa.VARCHAR(length=20), nullable=True),
    sa.Column('um_college_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('um_zdeptid', sa.VARCHAR(length=80), nullable=True),
    sa.Column('um_zdeptid_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('status_flg', sa.VARCHAR(length=1), nullable=False),
    sa.Column('job_terminated', sa.VARCHAR(length=1), nullable=True),
    sa.Column('last_date_worked', oracle.DATE(), nullable=True),
    sa.Column('job_entry_dt', oracle.DATE(), nullable=True),
    sa.Column('position_entry_dt', oracle.DATE(), nullable=True),
    sa.Column('effseq', sa.INTEGER(), nullable=False),
    sa.Column('position_nbr', sa.VARCHAR(length=8), nullable=False),
    sa.Column('rrc', sa.VARCHAR(length=20), nullable=True),
    sa.PrimaryKeyConstraint('emplid', 'empl_rcdno', 'effdt', 'effseq', 'position_nbr', 'empl_status', 'status_flg', 'jobcode', 'deptid', name='sys_c00387275')
    )
    op.create_table('pure_eligible_aff_job_chng_hst',
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('um_affiliate_id', sa.VARCHAR(length=2), nullable=True),
    sa.Column('effdt', oracle.DATE(), nullable=True),
    sa.Column('um_affil_relation', sa.VARCHAR(length=6), nullable=True),
    sa.Column('title', sa.VARCHAR(length=35), nullable=True),
    sa.Column('deptid', sa.VARCHAR(length=10), nullable=True),
    sa.Column('deptid_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('status', sa.VARCHAR(length=1), nullable=True),
    sa.Column('um_college', sa.VARCHAR(length=20), nullable=True),
    sa.Column('um_college_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('um_campus', sa.VARCHAR(length=20), nullable=True),
    sa.Column('um_zdeptid', sa.VARCHAR(length=80), nullable=True),
    sa.Column('um_zdeptid_descr', sa.VARCHAR(length=30), nullable=True),
    sa.Column('status_flg', sa.VARCHAR(length=1), nullable=True),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('emplid', 'timestamp', name='sys_c00387810')
    )
