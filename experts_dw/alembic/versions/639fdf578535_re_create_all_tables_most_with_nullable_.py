"""Re-create all tables, most with nullable columns.

Revision ID: 639fdf578535
Revises: f6fffe3865be
Create Date: 2017-03-09 13:23:29.945374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '639fdf578535'
down_revision = 'f6fffe3865be'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('mds_person',
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('emplid')
    )
    op.create_table('mds_person_first_name',
    sa.Column('first_name', sa.String(length=30), nullable=True),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('emplid', 'timestamp')
    )
    op.create_table('mds_person_instl_email_addr',
    sa.Column('instl_email_addr', sa.String(length=70), nullable=True),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('emplid', 'timestamp')
    )
    op.create_table('mds_person_internet_id',
    sa.Column('internet_id', sa.String(length=15), nullable=True),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('emplid', 'timestamp')
    )
    op.create_table('mds_person_last_name',
    sa.Column('last_name', sa.String(length=30), nullable=True),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('emplid', 'timestamp')
    )
    op.create_table('mds_person_middle_name',
    sa.Column('middle_name', sa.String(length=30), nullable=True),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('emplid', 'timestamp')
    )
    op.create_table('mds_person_name_suffix',
    sa.Column('name_suffix', sa.String(length=15), nullable=True),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('emplid', 'timestamp')
    )
    op.create_table('mds_person_preferred_name',
    sa.Column('preferred_name', sa.String(length=50), nullable=True),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('emplid', 'timestamp')
    )
    op.create_table('mds_person_primary_empl_rcdno',
    sa.Column('primary_empl_rcdno', sa.Integer(), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('primary_empl_rcdno', 'emplid', 'timestamp')
    )
    op.create_table('mds_person_scival_id',
    sa.Column('scival_id', sa.Integer(), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('scival_id')
    )
    op.create_table('mds_person_tenure_flag',
    sa.Column('tenure_flag', sa.String(length=1), nullable=True),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('emplid', 'timestamp')
    )
    op.create_table('mds_person_tenure_track_flag',
    sa.Column('tenure_track_flag', sa.String(length=1), nullable=True),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('emplid', 'timestamp')
    )

def downgrade():
    op.drop_table('mds_person_tenure_track_flag')
    op.drop_table('mds_person_tenure_flag')
    op.drop_table('mds_person_scival_id')
    op.drop_table('mds_person_primary_empl_rcdno')
    op.drop_table('mds_person_preferred_name')
    op.drop_table('mds_person_name_suffix')
    op.drop_table('mds_person_middle_name')
    op.drop_table('mds_person_last_name')
    op.drop_table('mds_person_internet_id')
    op.drop_table('mds_person_instl_email_addr')
    op.drop_table('mds_person_first_name')
    op.drop_table('mds_person')
