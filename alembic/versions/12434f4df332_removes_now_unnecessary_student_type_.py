"""Removes now unnecessary student_type_description from student orgs.

Revision ID: 12434f4df332
Revises: da2dd36ea102
Create Date: 2022-05-11 12:06:22.876445

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '12434f4df332'
down_revision = 'da2dd36ea102'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('pure_sync_student_org_association', 'student_type_description')
    op.drop_column('pure_sync_student_org_association_scratch', 'student_type_description')

def downgrade():
    op.add_column('pure_sync_student_org_association_scratch', sa.Column('student_type_description', sa.VARCHAR(length=1024), nullable=False))
    op.add_column('pure_sync_student_org_association', sa.Column('student_type_description', sa.VARCHAR(length=1024), nullable=False))
