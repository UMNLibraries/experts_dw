"""Makes author_collaboration.name nullable.

Revision ID: ed0d841d0d0c
Revises: 12434f4df332
Create Date: 2022-05-11 12:16:12.718317

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'ed0d841d0d0c'
down_revision = '12434f4df332'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('author_collaboration', 'name',
               existing_type=sa.VARCHAR(length=1024),
               nullable=True,
               existing_comment='The name of the author collaboration organization.')

def downgrade():
    op.alter_column('author_collaboration', 'name',
               existing_type=sa.VARCHAR(length=1024),
               nullable=False,
               existing_comment='The name of the author collaboration organization.')
