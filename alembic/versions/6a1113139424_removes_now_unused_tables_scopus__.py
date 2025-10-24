"""Removes now unused tables scopus_(abstract|citation)s_to_download

Revision ID: 6a1113139424
Revises: a98bdea48f7d
Create Date: 2025-10-24 10:56:09.385495

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '6a1113139424'
down_revision = 'a98bdea48f7d'
branch_labels = None
depends_on = None

def upgrade():
    op.drop_table('scopus_abstracts_to_download')
    op.drop_table('scopus_citations_to_download')

def downgrade():
    op.create_table('scopus_citations_to_download',
    sa.Column('scopus_id', sa.INTEGER(), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('scopus_id', name='pk_scopus_citations_to_download')
    )
    op.create_table('scopus_abstracts_to_download',
    sa.Column('scopus_id', sa.INTEGER(), nullable=False),
    sa.Column('inserted', oracle.DATE(), nullable=False),
    sa.Column('updated', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('scopus_id', name='pk_scopus_abstracts_to_download')
    )
