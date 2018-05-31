"""Removes master dataset (mds) tables.

Revision ID: 849c87f1c8e4
Revises: c1dc63b64dd8
Create Date: 2018-05-29 15:42:44.199108

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '849c87f1c8e4'
down_revision = 'c1dc63b64dd8'
branch_labels = None
depends_on = None

def upgrade():
    op.drop_table('mds_person_primary_empl_rcdno')
    op.drop_table('mds_person_scival_id')
    op.drop_table('mds_person_name_suffix')
    op.drop_table('mds_person_middle_name')
    op.drop_table('mds_person_last_name')
    op.drop_table('mds_person_tenure_track_flag')
    op.drop_table('mds_person_tenure_flag')
    op.drop_table('mds_person_internet_id')
    op.drop_table('mds_person_instl_email_addr')
    op.drop_table('mds_person_first_name')
    op.drop_table('mds_person_preferred_name')
    op.drop_table('mds_person_emplid')
    op.drop_table('mds_person')

def downgrade():
    op.create_table('mds_person',
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('uuid', name='sys_c00281368'),
    oracle_resolve_synonyms=False
    )
    op.create_table('mds_person_preferred_name',
    sa.Column('preferred_name', sa.VARCHAR(length=255), nullable=True),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['uuid'], ['mds_person.uuid'], name='sys_c00281879', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid', 'timestamp', name='sys_c00281707')
    )
    op.create_table('mds_person_first_name',
    sa.Column('first_name', sa.VARCHAR(length=100), nullable=True),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['uuid'], ['mds_person.uuid'], name='sys_c00281873', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid', 'timestamp', name='sys_c00281708')
    )
    op.create_table('mds_person_instl_email_addr',
    sa.Column('instl_email_addr', sa.VARCHAR(length=70), nullable=True),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['uuid'], ['mds_person.uuid'], name='sys_c00281874', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid', 'timestamp', name='sys_c00281718')
    )
    op.create_table('mds_person_internet_id',
    sa.Column('internet_id', sa.VARCHAR(length=15), nullable=True),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['uuid'], ['mds_person.uuid'], name='sys_c00281875', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid', 'timestamp', name='sys_c00281698')
    )
    op.create_table('mds_person_tenure_flag',
    sa.Column('tenure_flag', sa.VARCHAR(length=1), nullable=True),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['uuid'], ['mds_person.uuid'], name='sys_c00281882', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid', 'timestamp', name='sys_c00281719')
    )
    op.create_table('mds_person_last_name',
    sa.Column('last_name', sa.VARCHAR(length=100), nullable=True),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['uuid'], ['mds_person.uuid'], name='sys_c00281876', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid', 'timestamp', name='sys_c00281706')
    )
    op.create_table('mds_person_middle_name',
    sa.Column('middle_name', sa.VARCHAR(length=100), nullable=True),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['uuid'], ['mds_person.uuid'], name='sys_c00281877', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid', 'timestamp', name='sys_c00281716')
    )
    op.create_table('mds_person_name_suffix',
    sa.Column('name_suffix', sa.VARCHAR(length=30), nullable=True),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['uuid'], ['mds_person.uuid'], name='sys_c00281878', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid', 'timestamp', name='sys_c00281717')
    )
    op.create_table('mds_person_scival_id',
    sa.Column('scival_id', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['uuid'], ['mds_person.uuid'], name='sys_c00281881', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid', 'timestamp', name='sys_c00281722')
    )
    op.create_table('mds_person_emplid',
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=True),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['uuid'], ['mds_person.uuid'], name='sys_c00281865', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid', 'timestamp', name='sys_c00281734')
    )
    op.create_table('mds_person_primary_empl_rcdno',
    sa.Column('primary_empl_rcdno', sa.INTEGER(), nullable=True),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.Column('uuid', sa.VARCHAR(length=36), nullable=False),
    sa.ForeignKeyConstraint(['uuid'], ['mds_person.uuid'], name='sys_c00281880', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uuid', 'timestamp', name='sys_c00281721')
    )
