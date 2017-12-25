"""Adds PureEligibleAffJob(New|Previous).

Revision ID: 3263b202dade
Revises: b1937002bfcc
Create Date: 2017-12-25 11:35:11.795535

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '3263b202dade'
down_revision = 'b1937002bfcc'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_eligible_aff_job_new',
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('um_affiliate_id', sa.String(length=2), nullable=False),
    sa.Column('effdt', sa.DateTime(), nullable=False),
    sa.Column('um_affil_relation', sa.String(length=6), nullable=True),
    sa.Column('title', sa.String(length=35), nullable=True),
    sa.Column('deptid', sa.String(length=10), nullable=False),
    sa.Column('deptid_descr', sa.String(length=30), nullable=True),
    sa.Column('status', sa.String(length=1), nullable=True),
    sa.Column('um_college', sa.String(length=20), nullable=True),
    sa.Column('um_college_descr', sa.String(length=30), nullable=True),
    sa.Column('um_campus', sa.String(length=20), nullable=True),
    sa.Column('um_zdeptid', sa.String(length=80), nullable=True),
    sa.Column('um_zdeptid_descr', sa.String(length=30), nullable=True),
    sa.Column('status_flg', sa.String(length=1), nullable=True),
    sa.PrimaryKeyConstraint('emplid', 'um_affiliate_id', 'effdt', 'deptid')
    )
    op.create_table('pure_eligible_aff_job_previous',
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('um_affiliate_id', sa.String(length=2), nullable=False),
    sa.Column('effdt', sa.DateTime(), nullable=False),
    sa.Column('um_affil_relation', sa.String(length=6), nullable=True),
    sa.Column('title', sa.String(length=35), nullable=True),
    sa.Column('deptid', sa.String(length=10), nullable=False),
    sa.Column('deptid_descr', sa.String(length=30), nullable=True),
    sa.Column('status', sa.String(length=1), nullable=True),
    sa.Column('um_college', sa.String(length=20), nullable=True),
    sa.Column('um_college_descr', sa.String(length=30), nullable=True),
    sa.Column('um_campus', sa.String(length=20), nullable=True),
    sa.Column('um_zdeptid', sa.String(length=80), nullable=True),
    sa.Column('um_zdeptid_descr', sa.String(length=30), nullable=True),
    sa.Column('status_flg', sa.String(length=1), nullable=True),
    sa.PrimaryKeyConstraint('emplid', 'um_affiliate_id', 'effdt', 'deptid')
    )

def downgrade():
    op.drop_table('pure_eligible_aff_job_previous')
    op.drop_table('pure_eligible_aff_job_new')
