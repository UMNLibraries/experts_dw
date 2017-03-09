"""Drop all tables, so that they can be re-created with named constraints.

Revision ID: f6fffe3865be
Revises: 96024695ebd1
Create Date: 2017-03-09 12:56:20.828492

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = 'f6fffe3865be'
down_revision = '96024695ebd1'
branch_labels = None
depends_on = None


def upgrade():
#    op.drop_table('mds_person_internet_id')
#    op.drop_table('mds_person_middle_name')
#    op.drop_table('mds_person_last_name')
#    op.drop_table('mds_person_first_name')
#    op.drop_table('mds_person_name_suffix')
#    op.drop_table('mds_person_preferred_name')
#    op.drop_table('mds_person_instl_email_addr')
#    op.drop_table('mds_person_tenure_track_flag')
#    op.drop_table('mds_person_tenure_flag')
    op.drop_table('mds_person_primary_empl_rcdno')
#    op.drop_table('mds_person_scival_id')
    op.drop_table('mds_person')


def downgrade():
    op.create_table('mds_person',
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.PrimaryKeyConstraint('emplid', name='sys_c00255200'),
    oracle_resolve_synonyms=False
    )
    op.create_table('mds_person_scival_id',
    sa.Column('scival_id', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], name='SYS_C00255205'),
    sa.PrimaryKeyConstraint('scival_id', name='sys_c00255204')
    )
    op.create_table('mds_person_primary_empl_rcdno',
    sa.Column('primary_empl_rcdno', oracle.NUMBER(scale=0, asdecimal=False), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], name='SYS_C00263189'),
    sa.PrimaryKeyConstraint('primary_empl_rcdno', 'emplid', 'timestamp', name='sys_c00263188')
    )
    op.create_table('mds_person_tenure_flag',
    sa.Column('tenure_flag', sa.VARCHAR(length=1), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], name='SYS_C00263194'),
    sa.PrimaryKeyConstraint('tenure_flag', 'emplid', 'timestamp', name='sys_c00263193')
    )
    op.create_table('mds_person_tenure_track_flag',
    sa.Column('tenure_track_flag', sa.VARCHAR(length=1), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], name='SYS_C00263199'),
    sa.PrimaryKeyConstraint('tenure_track_flag', 'emplid', 'timestamp', name='sys_c00263198')
    )
    op.create_table('mds_person_instl_email_addr',
    sa.Column('instl_email_addr', sa.VARCHAR(length=15), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], name='SYS_C00263570'),
    sa.PrimaryKeyConstraint('instl_email_addr', 'emplid', 'timestamp', name='sys_c00263569')
    )
    op.create_table('mds_person_preferred_name',
    sa.Column('preferred_name', sa.VARCHAR(length=50), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], name='SYS_C00263558'),
    sa.PrimaryKeyConstraint('preferred_name', 'emplid', 'timestamp', name='sys_c00263557')
    )
    op.create_table('mds_person_name_suffix',
    sa.Column('name_suffix', sa.VARCHAR(length=15), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], name='SYS_C00263184'),
    sa.PrimaryKeyConstraint('name_suffix', 'emplid', 'timestamp', name='sys_c00263183')
    )
    op.create_table('mds_person_first_name',
    sa.Column('first_name', sa.VARCHAR(length=30), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], name='SYS_C00263159'),
    sa.PrimaryKeyConstraint('first_name', 'emplid', 'timestamp', name='sys_c00263158')
    )
    op.create_table('mds_person_last_name',
    sa.Column('last_name', sa.VARCHAR(length=30), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], name='SYS_C00263174'),
    sa.PrimaryKeyConstraint('last_name', 'emplid', 'timestamp', name='sys_c00263173')
    )
    op.create_table('mds_person_middle_name',
    sa.Column('middle_name', sa.VARCHAR(length=30), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], name='SYS_C00263179'),
    sa.PrimaryKeyConstraint('middle_name', 'emplid', 'timestamp', name='sys_c00263178')
    )
    op.create_table('mds_person_internet_id',
    sa.Column('internet_id', sa.VARCHAR(length=15), nullable=False),
    sa.Column('emplid', sa.VARCHAR(length=11), nullable=False),
    sa.Column('timestamp', oracle.DATE(), nullable=False),
    sa.ForeignKeyConstraint(['emplid'], ['mds_person.emplid'], name='SYS_C00263169'),
    sa.PrimaryKeyConstraint('internet_id', 'emplid', 'timestamp', name='sys_c00263168')
    )
