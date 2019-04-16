"""Puts all pre-existing table/column comments into Python.

Revision ID: 9cb087af6d8c
Revises: 260f721fd7e9
Create Date: 2019-04-16 15:15:48.068606

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '9cb087af6d8c'
down_revision = '260f721fd7e9'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('pub', 'citation_total',
               existing_type=sa.INTEGER(),
               comment='Number of citations of the item. We call it a "total" because Pure also provides citation counts per year, which we may decide to use later.',
               existing_comment='Number of citations of the item.',
               existing_nullable=True)
    op.alter_column('pub', 'pure_modified',
               existing_type=oracle.DATE(),
               comment='Date the associated record was last modified in Pure.',
               existing_nullable=True)
    op.alter_column('pub', 'pure_subtype',
               existing_type=sa.VARCHAR(length=50),
               comment='Publication subtype or sub-format of the item in Pure.',
               existing_nullable=True)
    op.alter_column('pub', 'pure_type',
               existing_type=sa.VARCHAR(length=50),
               comment='Publication type or format of the item in Pure.',
               existing_nullable=True)
    op.create_table_comment(
        'pub',
        'Research output. Named "pub", short for "publication", due to Oracle character-length limits.',
        existing_comment='Research output. Named "pub", short for "publication", due to Oracle character-lenght limits.',
        schema=None
    )
    op.alter_column('pure_org', 'pure_modified',
               existing_type=oracle.DATE(),
               comment='Date the associated record was last modified in Pure.',
               existing_nullable=True)

def downgrade():
    op.alter_column('pure_org', 'pure_modified',
               existing_type=oracle.DATE(),
               comment=None,
               existing_comment='Date the associated record was last modified in Pure.',
               existing_nullable=True)
    op.alter_column('pure_jobcode_default_override', 'profiled',
               existing_type=sa.Boolean(),
               type_=sa.INTEGER(),
               existing_nullable=False)
    op.create_table_comment(
        'pub',
        'Research output. Named "pub", short for "publication", due to Oracle character-lenght limits.',
        existing_comment='Research output. Named "pub", short for "publication", due to Oracle character-length limits.',
        schema=None
    )
    op.alter_column('pub', 'pure_type',
               existing_type=sa.VARCHAR(length=50),
               comment=None,
               existing_comment='Publication type or format of the item in Pure.',
               existing_nullable=True)
    op.alter_column('pub', 'pure_subtype',
               existing_type=sa.VARCHAR(length=50),
               comment=None,
               existing_comment='Publication subtype or sub-format of the item in Pure.',
               existing_nullable=True)
    op.alter_column('pub', 'pure_modified',
               existing_type=oracle.DATE(),
               comment=None,
               existing_comment='Date the associated record was last modified in Pure.',
               existing_nullable=True)
    op.alter_column('pub', 'citation_total',
               existing_type=sa.INTEGER(),
               comment='Number of citations of the item.',
               existing_comment='Number of citations of the item. We call it a "total" because Pure also provides citation counts per year, which we may decide to use later.',
               existing_nullable=True)
