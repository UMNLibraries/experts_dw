"""Makes all PureApiPub columns not null.

Revision ID: e1ff947af0c9
Revises: a682994747e0
Create Date: 2018-05-28 14:24:08.358698

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'e1ff947af0c9'
down_revision = 'a682994747e0'
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('pure_api_pub', 'created',
               existing_type=oracle.DATE(),
               nullable=False)
    op.alter_column('pure_api_pub', 'downloaded',
               existing_type=oracle.DATE(),
               nullable=False)
    op.alter_column('pure_api_pub', 'json',
               existing_type=sa.CLOB(),
               nullable=False)
    op.alter_column('pure_api_pub', 'modified',
               existing_type=oracle.DATE(),
               nullable=False)

def downgrade():
    op.alter_column('pure_api_pub', 'modified',
               existing_type=oracle.DATE(),
               nullable=True)
    op.alter_column('pure_api_pub', 'json',
               existing_type=sa.CLOB(),
               nullable=True)
    op.alter_column('pure_api_pub', 'downloaded',
               existing_type=oracle.DATE(),
               nullable=True)
    op.alter_column('pure_api_pub', 'created',
               existing_type=oracle.DATE(),
               nullable=True)
