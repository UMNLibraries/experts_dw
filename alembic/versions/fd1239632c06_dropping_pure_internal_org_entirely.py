"""Dropping pure_internal_org entirely.

Revision ID: fd1239632c06
Revises: d79bd28cc144
Create Date: 2017-05-03 09:18:32.181772

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'fd1239632c06'
down_revision = 'd79bd28cc144'
branch_labels = None
depends_on = None

def upgrade():
  op.drop_table('pure_internal_org')

def downgrade():
  op.create_table(
    'pure_internal_org',
    sa.Column('id', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('pure_id', sa.VARCHAR(length=50), nullable=False),
    sa.Column('type', sa.VARCHAR(length=25), nullable=True),
    sa.Column('name_en', sa.VARCHAR(length=255), nullable=True),
    sa.Column('parent_id', oracle.NUMBER(scale=0, asdecimal=False), nullable=True),
    sa.Column('lft', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('rgt', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('level', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('tree_id', oracle.NUMBER(scale=0, asdecimal=False), nullable=True)
  )
