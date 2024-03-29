"""Added person_scival_id table.

Revision ID: f486afeae516
Revises: 9b0f4cfad578
Create Date: 2017-02-14 13:37:18.849597

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f486afeae516'
down_revision = '9b0f4cfad578'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person_scival_id',
    sa.Column('scival_id', sa.Integer(), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['person.emplid'], ),
    sa.PrimaryKeyConstraint('scival_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('person_scival_id')
    # ### end Alembic commands ###
