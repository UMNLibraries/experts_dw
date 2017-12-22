"""Changed all master dataset table names to have an mds prefix.

Revision ID: f4d72a6748d5
Revises: 2fd08e3d1ff0
Create Date: 2017-02-16 13:08:01.355472

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'f4d72a6748d5'
down_revision = '2fd08e3d1ff0'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('person_scival_id','mds_person_scival_id')
    op.rename_table('person','mds_person')

def downgrade():
    op.rename_table('mds_person_scival_id','person_scival_id')
    op.rename_table('mds_person','person')
