"""Updates person and pure_org to use Pure db column lengths.

Revision ID: 3e1e72d65a75
Revises: 85d2ea452514
Create Date: 2019-04-11 11:01:59.207668

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import oracle

# revision identifiers, used by Alembic.
revision = '3e1e72d65a75'
down_revision = '85d2ea452514'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('person', 'first_name',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=1024),
               comment='The given name for the person.',
               existing_comment='The given name for the person.',
               existing_nullable=True)
    op.alter_column('person', 'last_name',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=1024),
               comment='The family name for the person.',
               existing_comment='The family name for the person.',
               existing_nullable=True)
    op.alter_column('person', 'pure_id',
               existing_type=sa.VARCHAR(length=11),
               type_=sa.String(length=1024),
               comment='Unique ID for the person in our [Elsevier Pure database](https://experts.umn.edu). For UMN persons whose data we loaded into the Elsevier predecessor product, SciVal, this will be the SciVal ID. For other UMN persons whose data we have loaded into Pure, this will be the UMN employee ID (emplid). For UMN-external persons, this will be NULL. Note that because we have not loaded data for all UMN persons into Pure, some UMN persons will be classified as external in Pure.',
               existing_comment='Unique ID for the person in our [Elsevier Pure database](https://experts.umn.edu). For UMN persons whose data we loaded into the Elsevier predecessor product, SciVal, this will be the SciVal ID. For other UMN persons whose data we have loaded into Pure, this will be the UMN employee ID (emplid). For UMN-external persons, this will be NULL. Note that because we have not loaded data for all UMN persons into Pure, some UMN persons will be classified as external in Pure.',
               existing_nullable=True)
    op.alter_column('pure_org', 'name_en',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=512),
               comment='Name of the organization. Called "name_en" to be consistent with Pure naming, and to indicate that this is an English name.',
               existing_comment='Name of the organization. Called "name_en" to be consistent with Pure naming, and to indicate that this is an English name.',
               existing_nullable=False)
    op.alter_column('pure_org', 'name_variant_en',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=1024),
               comment='An alternative name of the organization. Called "name_variant_en" to be consistent with Pure naming, and to indicate that this is an English name.',
               existing_comment='An alternative name of the organization. Called "name_variant_en" to be consistent with Pure naming, and to indicate that this is an English name.',
               existing_nullable=True)
    op.alter_column('pure_org', 'parent_pure_id',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=1024),
               comment='Unique ID for the parent organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations, and some UMN-internal organizations.',
               existing_comment='Unique ID for the parent organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations, and some UMN-internal organizations.',
               existing_nullable=True)
    op.alter_column('pure_org', 'parent_pure_uuid',
               existing_type=sa.VARCHAR(length=36),
               comment='Universally-unique ID for the parent organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations.',
               existing_comment='Universally-unique ID for the parent organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations.',
               existing_nullable=True)
    op.alter_column('pure_org', 'pure_id',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=1024),
               comment='Unique ID for the organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations, and some UMN-internal organizations.',
               existing_comment='Unique ID for the organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations, and some UMN-internal organizations.',
               existing_nullable=True)
    op.alter_column('pure_org', 'type',
               existing_type=sa.VARCHAR(length=25),
               type_=sa.String(length=1024),
               comment='"academic", "college", "corporate", "department", "government", "initiative", "institute", "medical", "private non-profit", "university", or "unknown"',
               existing_comment='"academic", "college", "corporate", "department", "government", "initiative", "institute", "medical", "private non-profit", "university", or "unknown"',
               existing_nullable=True)
    op.alter_column('pure_org', 'url',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=1024),
               comment='The website for the organization.',
               existing_comment='The website for the organization.',
               existing_nullable=True)

def downgrade():
    op.alter_column('pure_org', 'url',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=255),
               comment='The website for the organization.',
               existing_nullable=True)
    op.alter_column('pure_org', 'type',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=25),
               comment='"academic", "college", "corporate", "department", "government", "initiative", "institute", "medical", "private non-profit", "university", or "unknown"',
               existing_nullable=True)
    op.alter_column('pure_org', 'pure_id',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=50),
               comment='Unique ID for the organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations, and some UMN-internal organizations.',
               existing_nullable=True)
    op.alter_column('pure_org', 'parent_pure_id',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=50),
               comment='Unique ID for the parent organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations, and some UMN-internal organizations.',
               existing_nullable=True)
    op.alter_column('pure_org', 'name_variant_en',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=255),
               comment='An alternative name of the organization. Called "name_variant_en" to be consistent with Pure naming, and to indicate that this is an English name.',
               existing_nullable=True)
    op.alter_column('pure_org', 'name_en',
               existing_type=sa.String(length=512),
               type_=sa.VARCHAR(length=255),
               comment='Name of the organization. Called "name_en" to be consistent with Pure naming, and to indicate that this is an English name.',
               existing_nullable=False)
    op.alter_column('person', 'pure_id',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=11),
               comment='Unique ID for the person in our [Elsevier Pure database](https://experts.umn.edu). For UMN persons whose data we loaded into the Elsevier predecessor product, SciVal, this will be the SciVal ID. For other UMN persons whose data we have loaded into Pure, this will be the UMN employee ID (emplid). For UMN-external persons, this will be NULL. Note that because we have not loaded data for all UMN persons into Pure, some UMN persons will be classified as external in Pure.',
               existing_nullable=True)
    op.alter_column('person', 'last_name',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=100),
               comment='The family name for the person.',
               existing_nullable=True)
    op.alter_column('person', 'first_name',
               existing_type=sa.String(length=1024),
               type_=sa.VARCHAR(length=100),
               comment='The given name for the person.',
               existing_nullable=True)
