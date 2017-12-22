"""Add comments for remaining tables.

Revision ID: 88c66a1c82b5
Revises: 90f9eccab135
Create Date: 2017-06-12 12:59:28.337578

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '88c66a1c82b5'
down_revision = '90f9eccab135'
branch_labels = None
depends_on = None

def upgrade():
  # pub:
  op.execute("comment on column EXPERT.PUB.UUID is 'Universally-unique ID for the item, generated for this Experts@Minnesota database.'");
  op.execute("comment on column EXPERT.PUB.PURE_UUID is 'Universally-unique ID for the item in our [Elsevier Pure database](https://experts.umn.edu).'");

  # person:
  op.execute("comment on table EXPERT.PERSON is 'A person, usually an author of research outputs. May be internal or external to UMN.'");
  op.execute("comment on column EXPERT.PERSON.UUID is 'Universally-unique ID for the person, generated for this Experts@Minnesota database.'");
  op.execute("comment on column EXPERT.PERSON.PURE_UUID is 'Universally-unique ID for the person in our [Elsevier Pure database](https://experts.umn.edu).'");
  op.execute("comment on column EXPERT.PERSON.PURE_ID is 'Unique ID for the person in our [Elsevier Pure database](https://experts.umn.edu). For UMN persons whose data we loaded into the Elsevier predecessor product, SciVal, this will be the SciVal ID. For other UMN persons whose data we have loaded into Pure, this will be the UMN employee ID (emplid). For UMN-external persons, this will be NULL. Note that because we have not loaded data for all UMN persons into Pure, some UMN persons will be classified as external in Pure.'");
  op.execute("comment on column EXPERT.PERSON.ORCID is '[Open Researcher and Contributor ID](https://orcid.org/) for the person.'");
  op.execute("comment on column EXPERT.PERSON.SCOPUS_ID is 'Unique ID for the person in the [Elsevier Scopus database](https://www.elsevier.com/solutions/scopus).'");
  op.execute("comment on column EXPERT.PERSON.HINDEX is 'An index that attempts to measure both the productivity and impact of the published work of a scientist or scholar. Used only in some disciplines, so for many persons this will be NULL. [More info](https://blog.scopus.com/posts/the-scopus-h-index-what-s-it-all-about-part-i) on [blog.scopus.com](https://blog.scopus.com/posts/5-facts-about-scopus-and-the-h-index).'");
  op.execute("comment on column EXPERT.PERSON.EMPLID is 'UMN employee ID (emplid).'");
  op.execute("comment on column EXPERT.PERSON.INTERNET_ID is 'UMN internet ID.'");
  op.execute("comment on column EXPERT.PERSON.FIRST_NAME is 'The given name for the person.'");
  op.execute("comment on column EXPERT.PERSON.LAST_NAME is 'The family name for the person.'");
  op.execute("comment on column EXPERT.PERSON.PURE_INTERNAL is '\"Y\" if Pure classifies the person as UMN-internal, \"N\" otherwise. Note that, because we have not loaded data for all UMN persons into Pure, some UMN persons will be classified as external in Pure.'");

  # pure_org:
  op.execute("comment on table EXPERT.PURE_ORG is 'An organization (e.g. university, college, department, etc.) in Pure. May be internal or external to UMN. Pure requires all UMN-internal organizations to be part of a single hierarchy, with UMN itself as the root. Note that sometimes we combine multiple UMN departments into one Pure organization. UMN-external organizations are never part of a hierarchy in Pure, and Pure gives us limited information for them in general.'");
  op.execute("comment on column EXPERT.PURE_ORG.PURE_UUID is 'Universally-unique ID for the organization in our [Elsevier Pure database](https://experts.umn.edu).'");
  op.execute("comment on column EXPERT.PURE_ORG.PURE_ID is 'Unique ID for the organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations, and some UMN-internal organizations.'");
  op.execute("comment on column EXPERT.PURE_ORG.PARENT_PURE_UUID is 'Universally-unique ID for the parent organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations.'");
  op.execute("comment on column EXPERT.PURE_ORG.PARENT_PURE_ID is 'Unique ID for the parent organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations, and some UMN-internal organizations.'");
  op.execute("comment on column EXPERT.PURE_ORG.PURE_INTERNAL is '\"Y\" if Pure classifies the organization as UMN-internal, \"N\" otherwise.'");
  op.execute("comment on column EXPERT.PURE_ORG.TYPE is '\"academic\", \"college\", \"corporate\", \"department\", \"government\", \"initiative\", \"institute\", \"medical\", \"private non-profit\", \"university\", or \"unknown\"'");
  op.execute("comment on column EXPERT.PURE_ORG.NAME_EN is 'Name of the organization. Called \"name_en\" to be consistent with Pure naming, and to indicate that this is an English name.'");
  op.execute("comment on column EXPERT.PURE_ORG.NAME_VARIANT_EN is 'An alternative name of the organization. Called \"name_variant_en\" to be consistent with Pure naming, and to indicate that this is an English name.'");
  op.execute("comment on column EXPERT.PURE_ORG.URL is 'The website for the organization.'");

  # pure_internal_org:
  op.execute("comment on table EXPERT.PURE_INTERNAL_ORG is 'The hierarchy (tree) of Pure UMN-internal organizations. This tree uses [nested sets](https://en.wikipedia.org/wiki/Nested_set_model), as implemented by the Python package [sqlalchemy_mptt](https://pypi.python.org/pypi/sqlalchemy_mptt/). However, because Oracle supports [recursive queries](https://explainextended.com/2009/09/28/adjacency-list-vs-nested-sets-oracle/), this may not be the best implementation. Because parent-child relationships (adjacency lists) already exist in the PURE_ORG table, this entire table may be unnecessary and may go away.'");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.PURE_UUID is 'See the description in PURE_ORG.'");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.PURE_ID is 'See the description in PURE_ORG.'");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.NAME_EN is 'See the description in PURE_ORG.'");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.ID is 'The unique ID for the node. Defined by sqlalchemy_mptt.'");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.PARENT_ID is 'The unique ID for the parent of the node. Defined by sqlalchemy_mptt.'");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.LFT is 'The left number for the node. Defined by sqlalchemy_mptt.'");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.RGT is 'The right number for the node. Defined by sqlalchemy_mptt.'");
  op.execute("comment on column \"EXPERT\".\"PURE_INTERNAL_ORG\".\"level\" is 'The depth (i.e. generation) of this node in the tree. Defined by sqlalchemy_mptt.'");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.TREE_ID is 'The unique ID of the tree that contains the node. Defined by sqlalchemy_mptt, which supports multiple trees in a single table.'");

  # person_pure_org:
  op.execute("comment on table EXPERT.PERSON_PURE_ORG is 'Associates persons with their organizations.'");
  op.execute("comment on column EXPERT.PERSON_PURE_ORG.PERSON_UUID is 'Foreign key to PERSON.'");
  op.execute("comment on column EXPERT.PERSON_PURE_ORG.PURE_ORG_UUID is 'Foreign key to PURE_ORG.'");

  # pub_person:
  op.execute("comment on table EXPERT.PUB_PERSON is 'Associates research outputs with persons (authors).'");
  op.execute("comment on column EXPERT.PUB_PERSON.PUB_UUID is 'Foreign key to PUB.'");
  op.execute("comment on column EXPERT.PUB_PERSON.PERSON_UUID is 'Foreign key to PERSON.'");
  op.execute("comment on column EXPERT.PUB_PERSON.EMPLID is 'De-normalization column. See the description in PERSON.'");
  op.execute("comment on column EXPERT.PUB_PERSON.PERSON_ORDINAL is 'The position of the person in the author list for the research output in Pure.'");
  op.execute("comment on column EXPERT.PUB_PERSON.PERSON_ROLE is '\"author\" or \"editor\". Need to find Pure documentation on any other possible values.'");
  op.execute("comment on column EXPERT.PUB_PERSON.FIRST_NAME is 'The given name for the person as it appears in the author list for the research output in Pure. Note that this may be differ from PERSON.FIRST_NAME.'");
  op.execute("comment on column EXPERT.PUB_PERSON.LAST_NAME is 'The family name for the person as it appears in the author list for the research output in Pure. Note that this may be differ from PERSON.LAST_NAME.'");
  op.execute("comment on column EXPERT.PUB_PERSON.PERSON_PURE_INTERNAL is '\"Y\" if Pure classified the person as UMN-internal at the time of publication of the research output, \"N\" otherwise. Note that, because we have not loaded data for all UMN persons into Pure, some UMN persons will be classified as external in Pure.'");

  # pub_person_pure_org:
  op.execute("comment on table EXPERT.PUB_PERSON_PURE_ORG is 'Associates with persons with their organization affiliations at the time of publication of a research output.'");
  op.execute("comment on column EXPERT.PUB_PERSON_PURE_ORG.PUB_UUID is 'Foreign key to PUB.'");
  op.execute("comment on column EXPERT.PUB_PERSON_PURE_ORG.PERSON_UUID is 'Foreign key to PERSON.'");
  op.execute("comment on column EXPERT.PUB_PERSON_PURE_ORG.PURE_ORG_UUID is 'Foreign key to PURE_ORG.'");

  # umn_dept_pure_org:
  op.execute("comment on table EXPERT.UMN_DEPT_PURE_ORG is 'Associates UMN departments with Pure organizations. Note that many UMN departments may map to one Pure organization.'");
  op.execute("comment on column EXPERT.UMN_DEPT_PURE_ORG.UMN_DEPT_ID is 'Unique ID for the UMN department in PeopleSoft.'");
  op.execute("comment on column EXPERT.UMN_DEPT_PURE_ORG.UMN_DEPT_NAME is 'Name of the UMN department in PeopleSoft. De-normalization column.'");
  op.execute("comment on column EXPERT.UMN_DEPT_PURE_ORG.PURE_ORG_UUID is 'Foreign key to PURE_ORG.'");
  op.execute("comment on column EXPERT.UMN_DEPT_PURE_ORG.PURE_ORG_ID is 'De-normalization column. See the description in PURE_ORG.'");
  
  # umn_person_pure_org:
  op.execute("comment on table EXPERT.UMN_PERSON_PURE_ORG is 'Associates persons that Pure classifies as UMN-internal with Pure organizations. We use this table, in addition to PERSON_PURE_ORG, because Pure attaches far more data to UMN-internal persons, some of which we use to ensure row uniqueness. Note that there are four columns in the primary key: PURE_ORG_UUID, PERSON_UUID, JOB_DESCRIPTION, and START_DATE. This is because UMN-internal persons may change positions, and also organization affiliations, over time. There may be multiple rows for the same person in this table.'");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.PURE_ORG_UUID is 'Foreign key to PURE_ORG.'");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.PERSON_UUID is 'Foreign key to PERSON.'");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.JOB_DESCRIPTION is 'The description of this job in PeopleSoft. Maybe be better to use a job code here instead.'");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.START_DATE is 'The date the person started this job with this organization.'");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.END_DATE is 'The date the person ended this job with this organization.'");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.EMPLOYED_AS is 'Always \"Academic\" for the data we have loaded so far. Uncertain whether we will have other values in the future.'");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.STAFF_TYPE is '\"academic\" or \"nonacademic\".'");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.PRIMARY is '\"Y\" if this is the person\"s primary organization affiliation, otherwise \"N\".'");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.EMPLID is 'De-normalization column. See the description in PERSON.'");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.PURE_PERSON_ID is 'De-normalization column. See the description for PERSON.PURE_ID.'");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.PURE_ORG_ID is 'De-normalization column. See the description for PURE_ORG.PURE_ID.'");

def downgrade():
  # pub:
  op.execute("comment on column EXPERT.PUB.UUID is 'Primary key, generated for this Experts@Minnesota database.'");
  op.execute("comment on column EXPERT.PUB.PURE_UUID is 'Unique ID for the item in the Elsevier Pure product.'");

  # person:
  op.execute("comment on table EXPERT.PERSON is NULL");
  op.execute("comment on column EXPERT.PERSON.UUID is NULL");
  op.execute("comment on column EXPERT.PERSON.PURE_UUID is NULL");
  op.execute("comment on column EXPERT.PERSON.PURE_ID is NULL");
  op.execute("comment on column EXPERT.PERSON.ORCID is NULL");
  op.execute("comment on column EXPERT.PERSON.SCOPUS_ID is NULL");
  op.execute("comment on column EXPERT.PERSON.HINDEX is NULL");
  op.execute("comment on column EXPERT.PERSON.EMPLID is NULL");
  op.execute("comment on column EXPERT.PERSON.INTERNET_ID is NULL");
  op.execute("comment on column EXPERT.PERSON.FIRST_NAME is NULL");
  op.execute("comment on column EXPERT.PERSON.LAST_NAME is NULL");
  op.execute("comment on column EXPERT.PERSON.PURE_INTERNAL is NULL");

  # pure_org:
  op.execute("comment on table EXPERT.PURE_ORG is NULL");
  op.execute("comment on column EXPERT.PURE_ORG.PURE_UUID is NULL");
  op.execute("comment on column EXPERT.PURE_ORG.PURE_ID is NULL");
  op.execute("comment on column EXPERT.PURE_ORG.PARENT_PURE_UUID is NULL");
  op.execute("comment on column EXPERT.PURE_ORG.PARENT_PURE_ID is NULL");
  op.execute("comment on column EXPERT.PURE_ORG.PURE_INTERNAL is NULL");
  op.execute("comment on column EXPERT.PURE_ORG.TYPE is NULL");
  op.execute("comment on column EXPERT.PURE_ORG.NAME_EN is NULL");
  op.execute("comment on column EXPERT.PURE_ORG.NAME_VARIANT_EN is NULL");
  op.execute("comment on column EXPERT.PURE_ORG.URL is NULL");

  # pure_internal_org:
  op.execute("comment on table EXPERT.PURE_INTERNAL_ORG is NULL");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.PURE_UUID is NULL");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.PURE_ID is NULL");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.NAME_EN is NULL");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.ID is NULL");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.PARENT_ID is NULL");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.LFT is NULL");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.RGT is NULL");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.level is NULL");
  op.execute("comment on column EXPERT.PURE_INTERNAL_ORG.TREE_ID is NULL");

  # person_pure_org:
  op.execute("comment on table EXPERT.PERSON_PURE_ORG is NULL");
  op.execute("comment on column EXPERT.PERSON_PURE_ORG.PERSON_UUID is NULL");
  op.execute("comment on column EXPERT.PERSON_PURE_ORG.PURE_ORG_UUID is NULL");

  # pub_person:
  op.execute("comment on table EXPERT.PUB_PERSON is NULL");
  op.execute("comment on column EXPERT.PUB_PERSON.PUB_UUID is NULL");
  op.execute("comment on column EXPERT.PUB_PERSON.PERSON_UUID is NULL");
  op.execute("comment on column EXPERT.PUB_PERSON.EMPLID is NULL");
  op.execute("comment on column EXPERT.PUB_PERSON.PERSON_ORDINAL is NULL");
  op.execute("comment on column EXPERT.PUB_PERSON.PERSON_ROLE is NULL");
  op.execute("comment on column EXPERT.PUB_PERSON.FIRST_NAME is NULL");
  op.execute("comment on column EXPERT.PUB_PERSON.LAST_NAME is NULL");
  op.execute("comment on column EXPERT.PUB_PERSON.PERSON_PURE_INTERNAL is NULL");

  # pub_person_pure_org:
  op.execute("comment on table EXPERT.PUB_PERSON_PURE_ORG is NULL");
  op.execute("comment on column EXPERT.PUB_PERSON_PURE_ORG.PUB_UUID is NULL");
  op.execute("comment on column EXPERT.PUB_PERSON_PURE_ORG.PERSON_UUID is NULL");
  op.execute("comment on column EXPERT.PUB_PERSON_PURE_ORG.PURE_ORG_UUID is NULL");

  # umn_dept_pure_org:
  op.execute("comment on table EXPERT.UMN_DEPT_PURE_ORG is NULL");
  op.execute("comment on column EXPERT.UMN_DEPT_PURE_ORG.UMN_DEPT_ID is NULL");
  op.execute("comment on column EXPERT.UMN_DEPT_PURE_ORG.UMN_DEPT_NAME is NULL");
  op.execute("comment on column EXPERT.UMN_DEPT_PURE_ORG.PURE_ORG_UUID is NULL");
  op.execute("comment on column EXPERT.UMN_DEPT_PURE_ORG.PURE_ORG_ID is NULL");
  
  # umn_person_pure_org:
  op.execute("comment on table EXPERT.UMN_PERSON_PURE_ORG is NULL");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.PURE_ORG_UUID is NULL");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.PERSON_UUID is NULL");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.JOB_DESCRIPTION is NULL");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.START_DATE is NULL");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.END_DATE is NULL");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.EMPLOYED_AS is NULL");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.STAFF_TYPE is NULL");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.PRIMARY is NULL");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.EMPLID is NULL");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.PURE_PERSON_ID is NULL");
  op.execute("comment on column EXPERT.UMN_PERSON_PURE_ORG.PURE_ORG_ID is NULL");
