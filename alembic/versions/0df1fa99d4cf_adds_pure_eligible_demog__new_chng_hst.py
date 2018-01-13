"""Adds pure_eligible_demog_(new|chng_hst).

Revision ID: 0df1fa99d4cf
Revises: 6d206749ae9f
Create Date: 2018-01-13 16:15:52.253704

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '0df1fa99d4cf'
down_revision = '6d206749ae9f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('pure_eligible_demog_chng_hst',
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('internet_id', sa.String(length=15), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('middle_initial', sa.String(length=1), nullable=True),
    sa.Column('name_suffix', sa.String(length=3), nullable=True),
    sa.Column('instl_email_addr', sa.String(length=70), nullable=True),
    sa.Column('tenure_flag', sa.String(length=1), nullable=True),
    sa.Column('tenure_track_flag', sa.String(length=1), nullable=True),
    sa.Column('primary_empl_rcdno', sa.String(length=38), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('emplid', 'timestamp')
    )
    op.create_table('pure_eligible_demog_new',
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('internet_id', sa.String(length=15), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('middle_initial', sa.String(length=1), nullable=True),
    sa.Column('name_suffix', sa.String(length=3), nullable=True),
    sa.Column('instl_email_addr', sa.String(length=70), nullable=True),
    sa.Column('tenure_flag', sa.String(length=1), nullable=True),
    sa.Column('tenure_track_flag', sa.String(length=1), nullable=True),
    sa.Column('primary_empl_rcdno', sa.String(length=38), nullable=True),
    sa.PrimaryKeyConstraint('emplid')
    )
    op.drop_table('demographics_chng_hst')

def downgrade():
    op.create_table('demographics_chng_hst',
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('internet_id', sa.VARCHAR(length=15), nullable=True),
    sa.Column('name', sa.VARCHAR(length=50), nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=30), nullable=True),
    sa.Column('first_name', sa.VARCHAR(length=30), nullable=True),
    sa.Column('middle_initial', sa.VARCHAR(length=1), nullable=True),
    sa.Column('name_suffix', sa.VARCHAR(length=3), nullable=True),
    sa.Column('instl_email_addr', sa.VARCHAR(length=70), nullable=True),
    sa.Column('tenure_flag', sa.VARCHAR(length=1), nullable=True),
    sa.Column('tenure_track_flag', sa.VARCHAR(length=1), nullable=True),
    sa.Column('primary_empl_rcdno', sa.VARCHAR(length=38), nullable=True),
    sa.Column('um_directory_url', sa.VARCHAR(length=38), nullable=True),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('emplid', 'timestamp', name='sys_c00388007')
    )
    op.drop_table('pure_eligible_demog_new')
    op.drop_table('pure_eligible_demog_chng_hst')
