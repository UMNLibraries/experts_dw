"""Adds pure_sync_student_org_association_* tables.

Revision ID: da2dd36ea102
Revises: 288cc4c9669a
Create Date: 2022-03-02 15:04:39.129960

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'da2dd36ea102'
down_revision = '288cc4c9669a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_sync_student_org_association',
    sa.Column('student_org_association_id', sa.String(length=1024), nullable=False),
    sa.Column('person_id', sa.String(length=1024), nullable=False),
    sa.Column('period_start_date', sa.DateTime(), nullable=False),
    sa.Column('period_end_date', sa.DateTime(), nullable=True),
    sa.Column('org_id', sa.String(length=1024), nullable=False),
    sa.Column('status', sa.String(length=1024), nullable=False),
    sa.Column('affiliation_id', sa.String(length=30), nullable=True),
    sa.Column('student_type_description', sa.String(length=1024), nullable=False),
    sa.Column('email_address', sa.String(length=255), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.Column('modified', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['person_id'], ['pure_sync_person_data.person_id'], name=op.f('fk_pure_sync_student_org_association_person_id_pure_sync_person_data')),
    sa.PrimaryKeyConstraint('student_org_association_id', name=op.f('pk_pure_sync_student_org_association'))
    )
    op.create_table('pure_sync_student_org_association_scratch',
    sa.Column('student_org_association_id', sa.String(length=1024), nullable=False),
    sa.Column('person_id', sa.String(length=1024), nullable=False),
    sa.Column('period_start_date', sa.DateTime(), nullable=False),
    sa.Column('period_end_date', sa.DateTime(), nullable=True),
    sa.Column('org_id', sa.String(length=1024), nullable=False),
    sa.Column('status', sa.String(length=1024), nullable=False),
    sa.Column('affiliation_id', sa.String(length=30), nullable=True),
    sa.Column('student_type_description', sa.String(length=1024), nullable=False),
    sa.Column('email_address', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['person_id'], ['pure_sync_person_data.person_id'], name=op.f('fk_pure_sync_student_org_association_scratch_person_id_pure_sync_person_data')),
    sa.PrimaryKeyConstraint('student_org_association_id', name=op.f('pk_pure_sync_student_org_association_scratch'))
    )

def downgrade():
    op.drop_table('pure_sync_student_org_association_scratch')
    op.drop_table('pure_sync_student_org_association')
