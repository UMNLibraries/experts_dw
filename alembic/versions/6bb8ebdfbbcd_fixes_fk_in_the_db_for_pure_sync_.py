"""Fixes FK in the db for pure_sync_student_org_association_scratch.

Revision ID: 6bb8ebdfbbcd
Revises: ed0d841d0d0c
Create Date: 2022-05-15 09:08:58.038838

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '6bb8ebdfbbcd'
down_revision = 'ed0d841d0d0c'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('fk_pure_sync_student_org_association_scratch_person_id_pure_sync_person_data', 'pure_sync_student_org_association_scratch', type_='foreignkey')
    op.create_foreign_key(op.f('fk_pure_sync_student_org_association_scratch_person_id_pure_sync_person_data_scratch'), 'pure_sync_student_org_association_scratch', 'pure_sync_person_data_scratch', ['person_id'], ['person_id'])

def downgrade():
    op.drop_constraint(op.f('fk_pure_sync_student_org_association_scratch_person_id_pure_sync_person_data_scratch'), 'pure_sync_student_org_association_scratch', type_='foreignkey')
    op.create_foreign_key('fk_pure_sync_student_org_association_scratch_person_id_pure_sync_person_data', 'pure_sync_student_org_association_scratch', 'pure_sync_person_data', ['person_id'], ['person_id'])
