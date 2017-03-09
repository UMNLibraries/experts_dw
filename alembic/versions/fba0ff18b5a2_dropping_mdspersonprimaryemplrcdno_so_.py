"""Dropping MdsPersonPrimaryEmplRcdno so that it can be re-created.

Revision ID: fba0ff18b5a2
Revises: 639fdf578535
Create Date: 2017-03-09 13:57:26.890137

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'fba0ff18b5a2'
down_revision = '639fdf578535'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_table('mds_person_primary_empl_rcdno')

def downgrade():
    op.create_table('mds_person_primary_empl_rcdno',
    sa.Column('primary_empl_rcdno', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], name='SYS_C00264326'),
    sa.PrimaryKeyConstraint('primary_empl_rcdno', 'emplid', 'timestamp', name='sys_c00264325')
    )
