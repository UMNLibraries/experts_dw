"""Updates remaining tables to use Pure db column lengths.

Revision ID: 260f721fd7e9
Revises: 3e1e72d65a75
Create Date: 2019-04-11 12:58:54.706247

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '260f721fd7e9'
down_revision = '3e1e72d65a75'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('pub_person', 'first_name',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=1024),
               comment='The given name for the person as it appears in the author list for the research output in Pure. Note that this may be differ from PERSON.FIRST_NAME.',
               existing_comment='The given name for the person as it appears in the author list for the research output in Pure. Note that this may be differ from PERSON.FIRST_NAME.',
               existing_nullable=True)
    op.alter_column('pub_person', 'last_name',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=1024),
               comment='The family name for the person as it appears in the author list for the research output in Pure. Note that this may be differ from PERSON.LAST_NAME.',
               existing_comment='The family name for the person as it appears in the author list for the research output in Pure. Note that this may be differ from PERSON.LAST_NAME.',
               existing_nullable=True)
    op.alter_column('pure_internal_org', 'name_en',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=512),
               comment='See the description in PURE_ORG.',
               existing_comment='See the description in PURE_ORG.',
               existing_nullable=True)
    op.alter_column('pure_internal_org', 'pure_id',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=1024),
               comment='See the description in PURE_ORG.',
               existing_comment='See the description in PURE_ORG.',
               existing_nullable=True)
    op.alter_column('umn_dept_pure_org', 'pure_org_id',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=1024),
               comment='Unique ID for the organization in our [Elsevier Pure database](https://experts.umn.edu).',
               existing_comment='Unique ID for the organization in our [Elsevier Pure database](https://experts.umn.edu).',
               existing_nullable=False)
    op.alter_column('umn_person_pure_org', 'employed_as',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=1024),
               comment='Always "Academic" for the data we have loaded so far. Uncertain whether we will have other values in the future.',
               existing_comment='Always "Academic" for the data we have loaded so far. Uncertain whether we will have other values in the future.',
               existing_nullable=True)
    op.alter_column('umn_person_pure_org', 'job_description',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=1024),
               comment='The description of this job in PeopleSoft. Maybe be better to use a job code here instead.',
               existing_comment='The description of this job in PeopleSoft. Maybe be better to use a job code here instead.')
    op.alter_column('umn_person_pure_org', 'pure_org_id',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=1024),
               comment='De-normalization column. See the description for PURE_ORG.PURE_ID.',
               existing_comment='De-normalization column. See the description for PURE_ORG.PURE_ID.',
               existing_nullable=True)
    op.alter_column('umn_person_pure_org', 'staff_type',
               existing_type=sa.VARCHAR(length=11),
               type_=sa.String(length=1024),
               comment='"academic" or "nonacademic".',
               existing_comment='"academic" or "nonacademic".',
               existing_nullable=True)

def downgrade():
    op.alter_column('umn_person_pure_org', 'staff_type',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=11),
               comment='"academic" or "nonacademic".',
               existing_nullable=True)
    op.alter_column('umn_person_pure_org', 'pure_org_id',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=50),
               comment='De-normalization column. See the description for PURE_ORG.PURE_ID.',
               existing_nullable=True)
    op.alter_column('umn_person_pure_org', 'job_description',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=255),
               comment='The description of this job in PeopleSoft. Maybe be better to use a job code here instead.')
    op.alter_column('umn_person_pure_org', 'employed_as',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=50),
               comment='Always "Academic" for the data we have loaded so far. Uncertain whether we will have other values in the future.',
               existing_nullable=True)
    op.alter_column('umn_dept_pure_org', 'pure_org_id',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=50),
               comment='Unique ID for the organization in our [Elsevier Pure database](https://experts.umn.edu).',
               existing_nullable=False)
    op.alter_column('pure_internal_org', 'pure_id',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=50),
               comment='See the description in PURE_ORG.',
               existing_nullable=True)
    op.alter_column('pure_internal_org', 'name_en',
               existing_type=sa.String(length=512),
               type_=sa.VARCHAR(length=255),
               comment='See the description in PURE_ORG.',
               existing_nullable=True)
    op.alter_column('pub_person', 'last_name',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=100),
               comment='The family name for the person as it appears in the author list for the research output in Pure. Note that this may be differ from PERSON.LAST_NAME.',
               existing_nullable=True)
    op.alter_column('pub_person', 'first_name',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=100),
               comment='The given name for the person as it appears in the author list for the research output in Pure. Note that this may be differ from PERSON.FIRST_NAME.',
               existing_nullable=True)
