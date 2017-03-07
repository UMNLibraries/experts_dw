"""Generated code to create mds tables based on ps_dwhr_demo_addr.

Revision ID: 3aff4674ce03
Revises: 76eb2ee4ad8c
Create Date: 2017-03-04 14:53:16.574134

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3aff4674ce03'
down_revision = '76eb2ee4ad8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('mds_person_first_name',
    sa.Column('first_name', sa.String(length=30), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('first_name', 'emplid', 'timestamp')
    )
    op.create_table('mds_person_inst_email_addr',
    sa.Column('inst_email_addr', sa.String(length=15), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('inst_email_addr', 'emplid', 'timestamp')
    )
    op.create_table('mds_person_internet_id',
    sa.Column('internet_id', sa.String(length=15), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('internet_id', 'emplid', 'timestamp')
    )
    op.create_table('mds_person_last_name',
    sa.Column('last_name', sa.String(length=30), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('last_name', 'emplid', 'timestamp')
    )
    op.create_table('mds_person_middle_name',
    sa.Column('middle_name', sa.String(length=30), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('middle_name', 'emplid', 'timestamp')
    )
    op.create_table('mds_person_name_suffix',
    sa.Column('name_suffix', sa.String(length=15), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('name_suffix', 'emplid', 'timestamp')
    )
    op.create_table('mds_person_primary_empl_rcdno',
    sa.Column('primary_empl_rcdno', sa.Integer(), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('primary_empl_rcdno', 'emplid', 'timestamp')
    )
    op.create_table('mds_person_tenure_flag',
    sa.Column('tenure_flag', sa.String(length=1), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('tenure_flag', 'emplid', 'timestamp')
    )
    op.create_table('mds_person_tenure_track_flag',
    sa.Column('tenure_track_flag', sa.String(length=1), nullable=False),
    sa.Column('emplid', sa.String(length=11), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], ),
    sa.PrimaryKeyConstraint('tenure_track_flag', 'emplid', 'timestamp')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mds_person_tenure_track_flag')
    op.drop_table('mds_person_tenure_flag')
    op.drop_table('mds_person_primary_empl_rcdno')
    op.drop_table('mds_person_name_suffix')
    op.drop_table('mds_person_middle_name')
    op.drop_table('mds_person_last_name')
    op.drop_table('mds_person_internet_id')
    op.drop_table('mds_person_inst_email_addr')
    op.drop_table('mds_person_first_name')
    # ### end Alembic commands ###