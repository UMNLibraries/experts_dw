"""Adds author collaboration tables.

Revision ID: 9a7c302f1949
Revises: 9cb087af6d8c
Create Date: 2019-04-29 15:35:03.173105

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '9a7c302f1949'
down_revision = '9cb087af6d8c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('author_collaboration',
    sa.Column('uuid', sa.String(length=36), nullable=False, comment='Universally-unique ID for the author collaboration, generated for this Experts@Minnesota database.'),
    sa.Column('pure_uuid', sa.String(length=36), nullable=False, comment='Universally-unique ID for the author collaboration in our [Elsevier Pure database](https://experts.umn.edu).'),
    sa.Column('name', sa.String(length=1024), nullable=False, comment='The name of the author collaboration organization.'),
    sa.PrimaryKeyConstraint('uuid'),
    comment='An organization through which authors collaborate on research outputs.'
    )
    op.create_index(op.f('ix_author_collaboration_pure_uuid'), 'author_collaboration', ['pure_uuid'], unique=False)
    op.create_table('pub_author_collaboration',
    sa.Column('pub_uuid', sa.String(length=36), nullable=False, comment='Foreign key to PUB.'),
    sa.Column('author_collaboration_uuid', sa.String(length=36), nullable=False, comment='Foreign key to AUTHOR_COLLABORATION.'),
    sa.Column('author_ordinal', sa.Integer(), nullable=False, comment='The position of the author collaboration in the author list for the research output in Pure.'),
    sa.Column('author_role', sa.String(length=255), nullable=True, comment='"author" or "editor". Need to find Pure documentation on any other possible values.'),
    sa.ForeignKeyConstraint(['author_collaboration_uuid'], ['author_collaboration.uuid'], ),
    sa.ForeignKeyConstraint(['pub_uuid'], ['pub.uuid'], ),
    sa.PrimaryKeyConstraint('pub_uuid', 'author_collaboration_uuid'),
    comment='Associates research outputs with author collaborations (a type of author).'
    )

def downgrade():
    op.drop_table('pub_author_collaboration')
    op.drop_index(op.f('ix_author_collaboration_pure_uuid'), table_name='author_collaboration')
    op.drop_table('author_collaboration')
