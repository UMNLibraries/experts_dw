"""Converts some previously ad-hoc boolean columns to proper booleans.

Revision ID: 04d003b7ad71
Revises: 1fdd6c1c321e
Create Date: 2020-10-15 18:02:40.845695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04d003b7ad71'
down_revision = '1fdd6c1c321e'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('pub', 'eissued_current',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='eissued_current_bool'),
               existing_comment='True or false depending on whether this is a current state.',
               existing_nullable=True)
    op.alter_column('pub', 'inprep_current',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='inprep_current_bool'),
               existing_comment='True or false depending on whether this is a current state.',
               existing_nullable=True)
    op.alter_column('pub', 'inpress_current',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='inpress_current_bool'),
               existing_comment='True or false depending on whether this is a current state.',
               existing_nullable=True)
    op.alter_column('pub', 'issued_current',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='issued_current_bool'),
               existing_comment='True or false depending on whether this is a current state.',
               existing_nullable=True)
    op.alter_column('pub', 'submitted_current',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='submitted_current_bool'),
               existing_comment='True or false depending on whether this is a current state.',
               existing_nullable=True)
    op.alter_column('pub', 'unissued_current',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='unissued_current_bool'),
               existing_comment='True or false depending on whether this is a current state.',
               existing_nullable=True)
    op.alter_column('pure_eligible_affiliate_jobcode', 'default_profiled',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='default_profiled_bool'),
               existing_nullable=False)
    op.alter_column('pure_eligible_employee_jobcode', 'default_profiled',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='default_profiled_bool'),
               existing_nullable=False)
    op.alter_column('pure_eligible_employee_jobcode', 'default_profiled_overrideable',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='default_profiled_overrideable_bool'),
               existing_nullable=False)
    op.alter_column('pure_eligible_poi_jobcode', 'default_profiled',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='default_profiled_bool'),
               existing_nullable=False)
    op.alter_column('pure_employee_jobcode_default_override', 'profiled',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='profiled_bool'),
               existing_nullable=False)
    op.alter_column('pure_sync_person_data', 'profiled',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='profiled_bool'),
               existing_nullable=False)
    op.alter_column('pure_sync_person_data_scratch', 'profiled',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='profiled_bool'),
               existing_nullable=False)
    op.alter_column('pure_sync_staff_org_association', 'primary_association',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='primary_association_bool'),
               existing_nullable=False)
    op.alter_column('pure_sync_staff_org_association_scratch', 'primary_association',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='primary_association_bool'),
               existing_nullable=False)


def downgrade():
    op.alter_column('pure_sync_staff_org_association_scratch', 'primary_association',
               existing_type=sa.Boolean(name='primary_association_bool'),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('pure_sync_staff_org_association', 'primary_association',
               existing_type=sa.Boolean(name='primary_association_bool'),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('pure_sync_person_data_scratch', 'profiled',
               existing_type=sa.Boolean(name='profiled_bool'),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('pure_sync_person_data', 'profiled',
               existing_type=sa.Boolean(name='profiled_bool'),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('pure_employee_jobcode_default_override', 'profiled',
               existing_type=sa.Boolean(name='profiled_bool'),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('pure_eligible_poi_jobcode', 'default_profiled',
               existing_type=sa.Boolean(name='default_profiled_bool'),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('pure_eligible_employee_jobcode', 'default_profiled_overrideable',
               existing_type=sa.Boolean(name='default_profiled_overrideable_bool'),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('pure_eligible_employee_jobcode', 'default_profiled',
               existing_type=sa.Boolean(name='default_profiled_bool'),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('pure_eligible_affiliate_jobcode', 'default_profiled',
               existing_type=sa.Boolean(name='default_profiled_bool'),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.alter_column('pub', 'unissued_current',
               existing_type=sa.Boolean(name='unissued_current_bool'),
               type_=sa.INTEGER(),
               existing_comment='True or false depending on whether this is a current state.',
               existing_nullable=True)
    op.alter_column('pub', 'submitted_current',
               existing_type=sa.Boolean(name='submitted_current_bool'),
               type_=sa.INTEGER(),
               existing_comment='True or false depending on whether this is a current state.',
               existing_nullable=True)
    op.alter_column('pub', 'issued_current',
               existing_type=sa.Boolean(name='issued_current_bool'),
               type_=sa.INTEGER(),
               existing_comment='True or false depending on whether this is a current state.',
               existing_nullable=True)
    op.alter_column('pub', 'inpress_current',
               existing_type=sa.Boolean(name='inpress_current_bool'),
               type_=sa.INTEGER(),
               existing_comment='True or false depending on whether this is a current state.',
               existing_nullable=True)
    op.alter_column('pub', 'inprep_current',
               existing_type=sa.Boolean(name='inprep_current_bool'),
               type_=sa.INTEGER(),
               existing_comment='True or false depending on whether this is a current state.',
               existing_nullable=True)
    op.alter_column('pub', 'eissued_current',
               existing_type=sa.Boolean(name='eissued_current_bool'),
               type_=sa.INTEGER(),
               existing_comment='True or false depending on whether this is a current state.',
               existing_nullable=True)
