"""Adds pure_eligible_person_(new|chng_hst).

Revision ID: 92e3be308009
Revises: 821653b7d54c
Create Date: 2018-01-12 16:45:40.230565

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '92e3be308009'
down_revision = '821653b7d54c'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'pure_eligible_person_new',
        sa.Column('emplid', sa.String(length=11), nullable=False),
        sa.PrimaryKeyConstraint('emplid')
    )
    op.create_table(
        'pure_eligible_person_chng_hst',
        sa.Column('emplid', sa.String(length=11), nullable=False),
        sa.Column('timestamp', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('emplid')
    )

def downgrade():
    op.drop_table('pure_eligible_person_chng_hst')
    op.drop_table('pure_eligible_person_new')
