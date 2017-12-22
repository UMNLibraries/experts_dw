"""Re-creating MdsPersonPrimaryEmplRcdno correctly.

Revision ID: 225a5061088c
Revises: fba0ff18b5a2
Create Date: 2017-03-09 13:58:53.569176

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '225a5061088c'
down_revision = 'fba0ff18b5a2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('mds_person_primary_empl_rcdno',
    sa.Column('primary_empl_rcdno', sa.Integer(), nullable=True),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('emplid', 'timestamp')
    )

def downgrade():
    op.drop_table('mds_person_primary_empl_rcdno')
