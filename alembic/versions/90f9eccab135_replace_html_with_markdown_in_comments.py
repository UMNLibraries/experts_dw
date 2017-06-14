"""Replace HTML with Markdown in comments.

Revision ID: 90f9eccab135
Revises: 3c412a148a35
Create Date: 2017-06-12 12:22:43.586417

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '90f9eccab135'
down_revision = '3c412a148a35'
branch_labels = None
depends_on = None

def upgrade():
  op.execute("comment on column EXPERT.PUB.OWNER_PURE_ORG_UUID is 'Unique ID for the organization that owns the item in our [Elsevier Pure database](https://experts.umn.edu/).'");
  op.execute("comment on column EXPERT.PUB.SCOPUS_ID is 'Unique ID for the item in the [Elsevier Scopus database](https://www.elsevier.com/solutions/scopus).'");
  op.execute("comment on column EXPERT.PUB.PMID is 'Unique ID for the item in the [NCBI PubMed database](https://www.ncbi.nlm.nih.gov/pubmed/).'");
  op.execute("comment on column EXPERT.PUB.DOI is '[Digital Object Identifier](https://www.doi.org/) for the item.'");
  op.execute("comment on column EXPERT.PUB.TYPE is 'Publication type or format of the item. See the [CSL spec](http://docs.citationstyles.org/en/stable/specification.html#appendix-iii-types) for a list of values.'");
  op.execute("comment on column EXPERT.PUB.ISSN is '[International Standard Serial Number](http://www.issn.org/understanding-the-issn/what-is-an-issn/).'");
  op.execute("comment on column EXPERT.PUB.OWNER_PURE_ORG_UUID is 'Unique ID for the organization that owns the item in our [Elsevier Pure database](https://experts.umn.edu).'");

def downgrade():
  op.execute("comment on column EXPERT.PUB.OWNER_PURE_ORG_UUID is 'Unique ID for the organization that owns the item in our Elsevier Pure database (https://experts.umn.edu/).'");
  op.execute("comment on column EXPERT.PUB.SCOPUS_ID is 'Unique ID for the item in the Elsevier Scopus database (https://www.elsevier.com/solutions/scopus).'");
  op.execute("comment on column EXPERT.PUB.PMID is 'Unique ID for the item in the NCBI PubMed database (https://www.ncbi.nlm.nih.gov/pubmed/).'");
  op.execute("comment on column EXPERT.PUB.DOI is 'Digital Object Identifier (https://www.doi.org/) for the item.'");
  op.execute("comment on column EXPERT.PUB.TYPE is 'Publication type or format of the item. See http://docs.citationstyles.org/en/stable/specification.html#appendix-iii-types for a list of values.'");
  op.execute("comment on column EXPERT.PUB.ISSN is 'International Standard Serial Number (http://www.issn.org/understanding-the-issn/what-is-an-issn/).'");
  op.execute("comment on column EXPERT.PUB.OWNER_PURE_ORG_UUID is 'Unique ID for the organization that owns the item in our <a href=\"https://experts.umn.edu/\">Elsevier Pure database</a>.'");
