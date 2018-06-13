"""Increases column sizes of pub volume and issue.

Revision ID: 8562b82ae686
Revises: 18bdcc29c553
Create Date: 2018-06-13 13:20:03.463614

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '8562b82ae686'
down_revision = '18bdcc29c553'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('pub', 'issue',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=2000),
               existing_nullable=True)
    op.alter_column('pub', 'volume',
               existing_type=sa.VARCHAR(length=25),
               type_=sa.String(length=2000),
               existing_nullable=True)

def downgrade():
    op.alter_column('pub', 'volume',
               existing_type=sa.String(length=2000),
               type_=sa.VARCHAR(length=25),
               existing_nullable=True)
    op.alter_column('pub', 'issue',
               existing_type=sa.String(length=2000),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
