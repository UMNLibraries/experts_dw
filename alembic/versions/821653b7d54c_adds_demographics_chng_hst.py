"""Adds demographics_chng_hst.

Revision ID: 821653b7d54c
Revises: 3125317d28a2
Create Date: 2017-12-26 16:48:27.251292

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '821653b7d54c'
down_revision = '3125317d28a2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('demographics_chng_hst',
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
        sa.Column('um_directory_url', sa.String(length=38), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('emplid', 'timestamp')
    )

def downgrade():
    op.drop_table('demographics_chng_hst')
