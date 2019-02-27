"""Sets umn_dept_pure_org.pure_org_id.nullable to false.

Revision ID: 071a7e236cce
Revises: 902aea8c7e00
Create Date: 2019-02-27 11:32:19.545461

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '071a7e236cce'
down_revision = '902aea8c7e00'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('umn_dept_pure_org', 'pure_org_id',
               existing_type=sa.VARCHAR(length=50),
               nullable=False,
               comment='Unique ID for the organization in our [Elsevier Pure database](https://experts.umn.edu).',
               existing_comment='De-normalization column. See the description in PURE_ORG.')

def downgrade():
    op.alter_column('umn_dept_pure_org', 'pure_org_id',
               existing_type=sa.VARCHAR(length=50),
               nullable=True,
               comment='De-normalization column. See the description in PURE_ORG.')
