"""Increases size of pub.pages to accommodate unusually large values from Pure.

Revision ID: 5df53f647a97
Revises: b70efd38f7bf
Create Date: 2020-02-03 13:06:52.382678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5df53f647a97'
down_revision = 'b70efd38f7bf'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        'pub',
        'pages',
        existing_type=sa.VARCHAR(length=50),
        type_=sa.VARCHAR(length=100)
    )

def downgrade():
    op.alter_column(
        'pub',
        'pages',
        existing_type=sa.VARCHAR(length=100),
        type_=sa.VARCHAR(length=50)
    )
