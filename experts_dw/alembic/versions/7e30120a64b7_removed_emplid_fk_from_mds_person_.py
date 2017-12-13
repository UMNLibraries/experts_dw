"""Removed emplid FK from mds_person_scival_id.

Revision ID: 7e30120a64b7
Revises: b61362caeab4
Create Date: 2017-04-15 09:49:23.784135

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e30120a64b7'
down_revision = 'b61362caeab4'
branch_labels = None
depends_on = None

def upgrade():
    op.drop_constraint('SYS_C00281677', 'mds_person_scival_id', type_='foreignkey')
    op.drop_column('mds_person_scival_id', 'emplid')

def downgrade():
    op.add_column('mds_person_scival_id', sa.Column('emplid', sa.VARCHAR(length=11), nullable=False))
    op.create_foreign_key('SYS_C00281677', 'mds_person_scival_id', 'mds_person_emplid', ['emplid'], ['emplid'], ondelete="CASCADE")
