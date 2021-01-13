"""Renames FKs to use sqlalchemy naming conventions.

Revision ID: 18e150e7de63
Revises: aea6a3aad4a4
Create Date: 2020-10-15 15:19:43.200284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '18e150e7de63'
down_revision = 'aea6a3aad4a4'
branch_labels = None
depends_on = None

# The commented-out lines below are for tst constraint names, uncommented lines for prd constraint names.

def upgrade():
#    op.drop_constraint('sys_c00137766', 'pub', type_='foreignkey')
    op.drop_constraint('SYS_C00452522', 'pub', type_='foreignkey')
    op.create_foreign_key(op.f('fk_pub_owner_pure_org_uuid_pure_org'), 'pub', 'pure_org', ['owner_pure_org_uuid'], ['pure_uuid'])
#    op.drop_constraint('sys_c00138295', 'pure_internal_org', type_='foreignkey')
    op.drop_constraint('SYS_C00452524', 'pure_internal_org', type_='foreignkey')
    op.create_foreign_key(op.f('fk_pure_internal_org_pure_uuid_pure_org'), 'pure_internal_org', 'pure_org', ['pure_uuid'], ['pure_uuid'])


def downgrade():
    op.drop_constraint(op.f('fk_pure_internal_org_pure_uuid_pure_org'), 'pure_internal_org', type_='foreignkey')
#    op.create_foreign_key('sys_c00138295', 'pure_internal_org', 'pure_org', ['pure_uuid'], ['pure_uuid'], ondelete='CASCADE')
    op.create_foreign_key('SYS_C00452524', 'pure_internal_org', 'pure_org', ['pure_uuid'], ['pure_uuid'], ondelete='CASCADE')
    op.drop_constraint(op.f('fk_pub_owner_pure_org_uuid_pure_org'), 'pub', type_='foreignkey')
#    op.create_foreign_key('sys_c00137766', 'pub', 'pure_org', ['owner_pure_org_uuid'], ['pure_uuid'], ondelete='CASCADE')
    op.create_foreign_key('SYS_C00452522', 'pub', 'pure_org', ['owner_pure_org_uuid'], ['pure_uuid'], ondelete='CASCADE')
