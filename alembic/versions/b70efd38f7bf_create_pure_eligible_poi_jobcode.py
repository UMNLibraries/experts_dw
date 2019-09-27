"""create pure_eligible_poi_jobcode

Revision ID: b70efd38f7bf
Revises: 0abe014bc8b8
Create Date: 2019-09-27 13:29:50.938374

"""
from alembic import op
import sqlalchemy as sa
import experts_dw


# revision identifiers, used by Alembic.
revision = 'b70efd38f7bf'
down_revision = '0abe014bc8b8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_eligible_poi_jobcode',
        sa.Column('jobcode', sa.String(13), primary_key=True),
        sa.Column('jobcode_descr', sa.String(length=35), nullable=True),
        sa.Column('pure_job_description', sa.String(length=50), nullable=False),
        sa.Column('default_employed_as', sa.String(length=50), nullable=False),
        sa.Column('default_staff_type', sa.String(length=11), nullable=False),
        sa.Column('default_visibility', sa.String(length=10), nullable=False),
        sa.Column('default_profiled', sa.Boolean(), nullable=False)
    )
    seedrows = [
        {'jobcode': '9560', 'jobcode_descr': 'Post-Doctoral Fellow', 'pure_job_description': 'Post-Doctoral Fellow', 'default_employed_as': 'pit', 'default_staff_type': 'nonacademic', 'default_visibility': 'Public', 'default_profiled': 0},
        {'jobcode': '9561', 'jobcode_descr': 'Graduate School Fellow', 'pure_job_description': 'Graduate School Fellow', 'default_employed_as': 'student', 'default_staff_type': 'nonacademic', 'default_visibility': 'Restricted', 'default_profiled': 0},
        {'jobcode': '9562', 'jobcode_descr': 'Graduate School Trainee', 'pure_job_description': 'Graduate School Trainee', 'default_employed_as': 'student', 'default_staff_type': 'nonacademic', 'default_visibility': 'Restricted', 'default_profiled': 0},
        {'jobcode': '9564', 'jobcode_descr': 'Professional School Fellow', 'pure_job_description': 'Professional School Fellow', 'default_employed_as': 'pit', 'default_staff_type': 'nonacademic', 'default_visibility': 'Restricted', 'default_profiled': 0},
        {'jobcode': '9565', 'jobcode_descr': 'Professional School Trainee', 'pure_job_description': 'Professional School Trainee', 'default_employed_as': 'student', 'default_staff_type': 'nonacademic', 'default_visibility': 'Restricted', 'default_profiled': 0},
        {'jobcode': '9566', 'jobcode_descr': 'Gradualte Fellow-extrnly funded', 'pure_job_description': 'Graduate Fellow', 'default_employed_as': 'student', 'default_staff_type': 'nonacademic', 'default_visibility': 'Restricted', 'default_profiled': 0},
        {'jobcode': '9568', 'jobcode_descr': 'NIH-NRSA Medical Fellow', 'pure_job_description': 'NIH-NRSA Medical Fellow', 'default_employed_as': 'pit', 'default_staff_type': 'nonacademic', 'default_visibility': 'Public', 'default_profiled': 0},
        {'jobcode': '9569', 'jobcode_descr': 'NIH-NRSA Med Fellow-GradProg', 'pure_job_description': 'NIH-NRSA Med Fellow-GradProg', 'default_employed_as': 'student', 'default_staff_type': 'nonacademic', 'default_visibility': 'Restricted', 'default_profiled': 0},
        {'jobcode': '9583', 'jobcode_descr': 'NIH-NRSA Med Resident-GradProg', 'pure_job_description': 'NIH-NRSA Med Resident-GradProg', 'default_employed_as': 'student', 'default_staff_type': 'nonacademic', 'default_visibility': 'Restricted', 'default_profiled': 0}
    ]
    op.bulk_insert(experts_dw.models.PureEligiblePOIJobcode.__table__, seedrows, multiinsert=False)

def downgrade():
    op.drop_table('pure_eligible_poi_jobcode')
