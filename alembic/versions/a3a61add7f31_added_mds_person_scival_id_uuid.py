"""Added mds_person_scival_id.uuid.

Revision ID: a3a61add7f31
Revises: 198b571c5903
Create Date: 2017-04-13 19:25:37.446636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3a61add7f31'
down_revision = '198b571c5903'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('mds_person_scival_id', sa.Column('uuid', sa.String(length=36), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('mds_person_scival_id', 'uuid')
    # ### end Alembic commands ###
