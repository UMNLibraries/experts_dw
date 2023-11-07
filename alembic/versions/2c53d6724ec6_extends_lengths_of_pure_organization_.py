"""Extends lengths of pure organization names

Revision ID: 2c53d6724ec6
Revises: 9e8a142a7b62
Create Date: 2023-11-03 13:52:31.898510

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '2c53d6724ec6'
down_revision = '9e8a142a7b62'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('pure_internal_org', 'name_en',
               existing_type=sa.VARCHAR(length=512),
               type_=sa.String(length=1024),
               existing_comment='See the description in PURE_ORG.',
               existing_nullable=True)
    op.alter_column('pure_org', 'name_en',
               existing_type=sa.VARCHAR(length=512),
               type_=sa.String(length=1024),
               existing_comment='Name of the organization. Called "name_en" to be consistent with Pure naming, and to indicate that this is an English name.',
               existing_nullable=False)

def downgrade():
    op.alter_column('pure_org', 'name_en',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=512),
               existing_comment='Name of the organization. Called "name_en" to be consistent with Pure naming, and to indicate that this is an English name.',
               existing_nullable=False)
    op.alter_column('pure_internal_org', 'name_en',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=512),
               existing_comment='See the description in PURE_ORG.',
               existing_nullable=True)
