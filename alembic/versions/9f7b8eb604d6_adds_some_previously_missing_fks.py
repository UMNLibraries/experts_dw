"""Adds some previously missing FKs.

Revision ID: 9f7b8eb604d6
Revises: 18e150e7de63
Create Date: 2020-10-15 15:42:28.077470

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f7b8eb604d6'
down_revision = '18e150e7de63'
branch_labels = None
depends_on = None


def upgrade():
    op.create_foreign_key(op.f('fk_person_pure_org_person_uuid_person'), 'person_pure_org', 'person', ['person_uuid'], ['uuid'])
    op.create_foreign_key(op.f('fk_person_pure_org_pure_org_uuid_pure_org'), 'person_pure_org', 'pure_org', ['pure_org_uuid'], ['pure_uuid'])
    op.create_foreign_key(op.f('fk_person_scopus_id_person_uuid_person'), 'person_scopus_id', 'person', ['person_uuid'], ['uuid'])
    op.create_foreign_key(op.f('fk_pub_person_person_uuid_person'), 'pub_person', 'person', ['person_uuid'], ['uuid'])
    op.create_foreign_key(op.f('fk_pub_person_pure_org_person_uuid_person'), 'pub_person_pure_org', 'person', ['person_uuid'], ['uuid'])
    op.create_foreign_key(op.f('fk_pub_person_pure_org_pure_org_uuid_pure_org'), 'pub_person_pure_org', 'pure_org', ['pure_org_uuid'], ['pure_uuid'])
    op.create_foreign_key(op.f('fk_umn_dept_pure_org_pure_org_uuid_pure_org'), 'umn_dept_pure_org', 'pure_org', ['pure_org_uuid'], ['pure_uuid'])
    op.create_foreign_key(op.f('fk_umn_person_pure_org_pure_org_uuid_pure_org'), 'umn_person_pure_org', 'pure_org', ['pure_org_uuid'], ['pure_uuid'])
    op.create_foreign_key(op.f('fk_umn_person_pure_org_person_uuid_person'), 'umn_person_pure_org', 'person', ['person_uuid'], ['uuid'])


def downgrade():
    op.drop_constraint(op.f('fk_umn_person_pure_org_person_uuid_person'), 'umn_person_pure_org', type_='foreignkey')
    op.drop_constraint(op.f('fk_umn_person_pure_org_pure_org_uuid_pure_org'), 'umn_person_pure_org', type_='foreignkey')
    op.drop_constraint(op.f('fk_umn_dept_pure_org_pure_org_uuid_pure_org'), 'umn_dept_pure_org', type_='foreignkey')
    op.drop_constraint(op.f('fk_pub_person_pure_org_pure_org_uuid_pure_org'), 'pub_person_pure_org', type_='foreignkey')
    op.drop_constraint(op.f('fk_pub_person_pure_org_person_uuid_person'), 'pub_person_pure_org', type_='foreignkey')
    op.drop_constraint(op.f('fk_pub_person_person_uuid_person'), 'pub_person', type_='foreignkey')
    op.drop_constraint(op.f('fk_person_scopus_id_person_uuid_person'), 'person_scopus_id', type_='foreignkey')
    op.drop_constraint(op.f('fk_person_pure_org_pure_org_uuid_pure_org'), 'person_pure_org', type_='foreignkey')
    op.drop_constraint(op.f('fk_person_pure_org_person_uuid_person'), 'person_pure_org', type_='foreignkey')
