"""Makes pub.issued(_precision) nullable.

Revision ID: 24b4a9a1bb8e
Revises: 08cf8f0d9321
Create Date: 2019-06-10 14:30:45.341308

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '24b4a9a1bb8e'
down_revision = '08cf8f0d9321'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('pub', 'issued',
               existing_type=oracle.DATE(),
               nullable=True,
               existing_comment='Date the item was issued/published.')
    op.alter_column('pub', 'issued_precision',
               existing_type=sa.INTEGER(),
               nullable=True,
               existing_comment='Precision of the ISSUED column, in days: 366 (year), 31 (month), 1 (day).')

def downgrade():
    op.alter_column('pub', 'issued_precision',
               existing_type=sa.INTEGER(),
               nullable=False,
               existing_comment='Precision of the ISSUED column, in days: 366 (year), 31 (month), 1 (day).')
    op.alter_column('pub', 'issued',
               existing_type=oracle.DATE(),
               nullable=False,
               existing_comment='Date the item was issued/published.')
