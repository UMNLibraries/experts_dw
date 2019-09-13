"""add columns to pure_eligible_affiliate_jobcode

Revision ID: 272054f1c058
Revises: 24082a82c949
Create Date: 2019-09-13 13:36:45.863318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '272054f1c058'
down_revision = '24082a82c949'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('pure_eligible_affiliate_jobcode', sa.Column('jobcode_descr', sa.String(length=35), nullable=True))
    op.add_column('pure_eligible_affiliate_jobcode', sa.Column('pure_job_description', sa.String(length=50), nullable=True))
    op.add_column('pure_eligible_affiliate_jobcode', sa.Column('default_employed_as', sa.String(length=50), nullable=True))
    op.add_column('pure_eligible_affiliate_jobcode', sa.Column('default_staff_type', sa.String(length=11), nullable=True))
    op.add_column('pure_eligible_affiliate_jobcode', sa.Column('default_visibility', sa.String(length=10), nullable=True))
    op.add_column('pure_eligible_affiliate_jobcode', sa.Column('default_profiled', sa.Boolean(), nullable=True))

    # Copy jobcode row data from pure_eligible_jobcode to pure_eligible_affiliate_jobcode
    sql = '''
    UPDATE pure_eligible_affiliate_jobcode
    SET (jobcode_descr, pure_job_description, default_employed_as, default_staff_type, default_visibility, default_profiled)
        = (
            SELECT jobcode_descr, pure_job_description, default_employed_as, default_staff_type, default_visibility, default_profiled
            FROM pure_eligible_jobcode
            WHERE
                pure_eligible_affiliate_jobcode.jobcode = pure_eligible_jobcode.jobcode
                AND pure_eligible_jobcode.jobcode IN ('9401A','9402A','9403A')
          )
    '''
    op.execute(sql)

    op.alter_column('pure_eligible_affiliate_jobcode', 'pure_job_description', nullable=False)
    op.alter_column('pure_eligible_affiliate_jobcode', 'default_employed_as', nullable=False)
    op.alter_column('pure_eligible_affiliate_jobcode', 'default_staff_type', nullable=False)
    op.alter_column('pure_eligible_affiliate_jobcode', 'default_visibility', nullable=False)
    op.alter_column('pure_eligible_affiliate_jobcode', 'default_profiled', nullable=False)

def downgrade():
    op.drop_column('pure_eligible_affiliate_jobcode', 'jobcode_descr')
    op.drop_column('pure_eligible_affiliate_jobcode', 'pure_job_description')
    op.drop_column('pure_eligible_affiliate_jobcode', 'default_employed_as')
    op.drop_column('pure_eligible_affiliate_jobcode', 'default_staff_type')
    op.drop_column('pure_eligible_affiliate_jobcode', 'default_visibility')
    op.drop_column('pure_eligible_affiliate_jobcode', 'default_profiled')
