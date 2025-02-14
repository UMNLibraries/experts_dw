"""Removes updated_count column from scopus_authored_abstracts_to_download

Revision ID: 43932648fc85
Revises: 0f4868faa337
Create Date: 2024-08-29 14:28:32.819391

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '43932648fc85'
down_revision = '0f4868faa337'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('scopus_authored_abstracts_to_download', 'updated_count')

def downgrade():
    op.add_column('scopus_authored_abstracts_to_download', sa.Column('updated_count', sa.INTEGER(), nullable=False))
