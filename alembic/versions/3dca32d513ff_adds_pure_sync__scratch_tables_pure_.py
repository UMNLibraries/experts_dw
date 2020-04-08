"""Adds pure_sync*_scratch tables, pure_sync*(created|modified) columns.

Revision ID: 3dca32d513ff
Revises: 095d39509575
Create Date: 2020-04-03 14:27:09.240599

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '3dca32d513ff'
down_revision = '095d39509575'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_sync_person_data_scratch',
    sa.Column('person_id', sa.String(length=1024), nullable=False),
    sa.Column('first_name', sa.String(length=1024), nullable=True),
    sa.Column('last_name', sa.String(length=1024), nullable=False),
    sa.Column('visibility', sa.String(length=1024), nullable=False),
    sa.Column('profiled', sa.Boolean(name='profiled_bool'), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('internet_id', sa.String(length=15), nullable=True),
    sa.Column('postnominal', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('person_id', name=op.f('pk_pure_sync_person_data_scratch')),
    comment='Scratch table for pure_sync_person_data.'
    )

    op.create_table('pure_sync_staff_org_association_scratch',
    sa.Column('staff_org_association_id', sa.String(length=1024), nullable=False),
    sa.Column('person_id', sa.String(length=1024), nullable=False),
    sa.Column('period_start_date', sa.DateTime(), nullable=False),
    sa.Column('period_end_date', sa.DateTime(), nullable=True),
    sa.Column('org_id', sa.String(length=1024), nullable=False),
    sa.Column('employment_type', sa.String(length=1024), nullable=False),
    sa.Column('staff_type', sa.String(length=1024), nullable=False),
    sa.Column('visibility', sa.String(length=1024), nullable=False),
    sa.Column('primary_association', sa.Boolean(name='primary_association_bool'), nullable=False),
    sa.Column('job_description', sa.String(length=1024), nullable=False),
    sa.Column('affiliation_id', sa.String(length=30), nullable=True),
    sa.ForeignKeyConstraint(['person_id'], ['pure_sync_person_data_scratch.person_id'], name=op.f('fk_pure_sync_staff_org_association_scratch_person_id_pure_sync_person_data_scratch')),
    sa.PrimaryKeyConstraint('staff_org_association_id', name=op.f('pk_pure_sync_staff_org_association_scratch')),
    comment='Scratch table for pure_sync_staff_org_association.'
    )

    op.create_table('pure_sync_user_data_scratch',
    sa.Column('person_id', sa.String(length=1024), nullable=False),
    sa.Column('first_name', sa.String(length=1024), nullable=True),
    sa.Column('last_name', sa.String(length=1024), nullable=True),
    sa.Column('user_name', sa.String(length=1024), nullable=False),
    sa.Column('email', sa.String(length=1024), nullable=False),
    sa.ForeignKeyConstraint(['person_id'], ['pure_sync_person_data_scratch.person_id'], name=op.f('fk_pure_sync_user_data_scratch_person_id_pure_sync_person_data_scratch')),
    sa.PrimaryKeyConstraint('person_id', name=op.f('pk_pure_sync_user_data_scratch')),
    comment='Scratch table for pure_sync_user_data.'
    )

    op.add_column('pure_sync_person_data', sa.Column('created', sa.DateTime(), nullable=True))
    op.add_column('pure_sync_person_data', sa.Column('modified', sa.DateTime(), nullable=True))
    op.alter_column('pure_sync_person_data', 'profiled',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='profiled_bool'),
               existing_nullable=False)

    op.add_column('pure_sync_staff_org_association', sa.Column('created', sa.DateTime(), nullable=True))
    op.add_column('pure_sync_staff_org_association', sa.Column('modified', sa.DateTime(), nullable=True))
    op.alter_column('pure_sync_staff_org_association', 'primary_association',
               existing_type=sa.INTEGER(),
               type_=sa.Boolean(name='primary_association_bool'),
               existing_nullable=False)

    op.add_column('pure_sync_user_data', sa.Column('created', sa.DateTime(), nullable=True))
    op.add_column('pure_sync_user_data', sa.Column('modified', sa.DateTime(), nullable=True))

def downgrade():
    op.drop_column('pure_sync_user_data', 'modified')
    op.drop_column('pure_sync_user_data', 'created')
    op.alter_column('pure_sync_staff_org_association', 'primary_association',
               existing_type=sa.Boolean(name='primary_association_bool'),
               type_=sa.INTEGER(),
               existing_nullable=False)

    op.drop_column('pure_sync_staff_org_association', 'modified')
    op.drop_column('pure_sync_staff_org_association', 'created')
    op.alter_column('pure_sync_person_data', 'profiled',
               existing_type=sa.Boolean(name='profiled_bool'),
               type_=sa.INTEGER(),
               existing_nullable=False)

    op.drop_column('pure_sync_person_data', 'modified')
    op.drop_column('pure_sync_person_data', 'created')

    op.drop_table('pure_sync_user_data_scratch')
    op.drop_table('pure_sync_staff_org_association_scratch')
    op.drop_table('pure_sync_person_data_scratch')
