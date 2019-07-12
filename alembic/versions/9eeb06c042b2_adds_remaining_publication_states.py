"""Adds remaining publication states.

Revision ID: 9eeb06c042b2
Revises: 24b4a9a1bb8e
Create Date: 2019-06-12 16:18:06.645402

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '9eeb06c042b2'
down_revision = '24b4a9a1bb8e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('pub', sa.Column('eissued', sa.DateTime(), nullable=True, comment='Date the item was/will be electronically issued/published, possibly ahead of print.'))
    op.add_column('pub', sa.Column('eissued_current', sa.Boolean(), nullable=True, comment='True or false depending on whether this is a current state.'))
    op.add_column('pub', sa.Column('eissued_precision', sa.Integer(), nullable=True, comment='Precision of the EISSUED column, in days: 366 (year), 31 (month), 1 (day).'))
    op.add_column('pub', sa.Column('inprep', sa.DateTime(), nullable=True, comment='Date the item was/will be in preparation to be issued/published.'))
    op.add_column('pub', sa.Column('inprep_current', sa.Boolean(), nullable=True, comment='True or false depending on whether this is a current state.'))
    op.add_column('pub', sa.Column('inprep_precision', sa.Integer(), nullable=True, comment='Precision of the INPREP column, in days: 366 (year), 31 (month), 1 (day).'))
    op.add_column('pub', sa.Column('inpress', sa.DateTime(), nullable=True, comment='Date the item was/will be accepted/in press.'))
    op.add_column('pub', sa.Column('inpress_current', sa.Boolean(), nullable=True, comment='True or false depending on whether this is a current state.'))
    op.add_column('pub', sa.Column('inpress_precision', sa.Integer(), nullable=True, comment='Precision of the INPRESS column, in days: 366 (year), 31 (month), 1 (day).'))
    op.add_column('pub', sa.Column('issued_current', sa.Boolean(), nullable=True, comment='True or false depending on whether this is a current state.'))
    op.add_column('pub', sa.Column('submitted', sa.DateTime(), nullable=True, comment='Date the item was/will be submitted to be issued/published.'))
    op.add_column('pub', sa.Column('submitted_current', sa.Boolean(), nullable=True, comment='True or false depending on whether this is a current state.'))
    op.add_column('pub', sa.Column('submitted_precision', sa.Integer(), nullable=True, comment='Precision of the SUBMITTED column, in days: 366 (year), 31 (month), 1 (day).'))
    op.add_column('pub', sa.Column('unissued', sa.DateTime(), nullable=True, comment='Date the item was/will be unissued/unpublished.'))
    op.add_column('pub', sa.Column('unissued_current', sa.Boolean(), nullable=True, comment='True or false depending on whether this is a current state.'))
    op.add_column('pub', sa.Column('unissued_precision', sa.Integer(), nullable=True, comment='Precision of the UNISSUED column, in days: 366 (year), 31 (month), 1 (day).'))
    op.alter_column('pub', 'issued',
               existing_type=oracle.DATE(),
               comment='Date the item was/will be issued/published.',
               existing_comment='Date the item was issued/published.',
               existing_nullable=True)

def downgrade():
    op.alter_column('pub', 'issued',
               existing_type=oracle.DATE(),
               comment='Date the item was issued/published.',
               existing_comment='Date the item was/will be issued/published.',
               existing_nullable=True)
    op.drop_column('pub', 'unissued_precision')
    op.drop_column('pub', 'unissued_current')
    op.drop_column('pub', 'unissued')
    op.drop_column('pub', 'submitted_precision')
    op.drop_column('pub', 'submitted_current')
    op.drop_column('pub', 'submitted')
    op.drop_column('pub', 'issued_current')
    op.drop_column('pub', 'inpress_precision')
    op.drop_column('pub', 'inpress_current')
    op.drop_column('pub', 'inpress')
    op.drop_column('pub', 'inprep_precision')
    op.drop_column('pub', 'inprep_current')
    op.drop_column('pub', 'inprep')
    op.drop_column('pub', 'eissued_precision')
    op.drop_column('pub', 'eissued_current')
    op.drop_column('pub', 'eissued')
