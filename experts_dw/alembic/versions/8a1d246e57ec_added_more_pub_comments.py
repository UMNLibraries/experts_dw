"""Added more pub comments.

Revision ID: 8a1d246e57ec
Revises: 92f0c5bb4344
Create Date: 2017-06-10 15:20:02.303142

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '8a1d246e57ec'
down_revision = '92f0c5bb4344'
branch_labels = None
depends_on = None

def upgrade():
  op.execute("comment on column EXPERT.PUB.PURE_UUID is 'Unique ID for the item in the Elsevier Pure product.'");
  op.execute("comment on column EXPERT.PUB.OWNER_PURE_ORG_UUID is 'Unique ID for the organization that owns the item in our Elsevier Pure database (https://experts.umn.edu/).'");
  op.execute("comment on column EXPERT.PUB.SCOPUS_ID is 'Unique ID for the item in the Elsevier Scopus database (https://www.elsevier.com/solutions/scopus).'");
  op.execute("comment on column EXPERT.PUB.PMID is 'Unique ID for the item in the NCBI PubMed database (https://www.ncbi.nlm.nih.gov/pubmed/).'");
  op.execute("comment on column EXPERT.PUB.DOI is 'Digital Object Identifier (https://www.doi.org/) for the item.'");
  op.execute("comment on column EXPERT.PUB.TYPE is 'Publication type or format of the item. See http://docs.citationstyles.org/en/stable/specification.html#appendix-iii-types for a list of values.'");
  op.execute("comment on column EXPERT.PUB.ISSUED is 'Date the item was issued/published.'");
  op.execute("comment on column EXPERT.PUB.ISSUED_PRECISION is 'Precision of the ISSUED column, in days: 366 (year), 31 (month), 1 (day).'");
  op.execute("comment on column EXPERT.PUB.TITLE is 'Primary title of the item.'");
  op.execute("comment on column EXPERT.PUB.CONTAINER_TITLE is 'Title of the container holding the item (e.g. the book title for a book chapter, the journal title for a journal article).'");
  op.execute("comment on column EXPERT.PUB.ISSN is 'International Standard Serial Number (http://www.issn.org/understanding-the-issn/what-is-an-issn/).'");
  op.execute("comment on column EXPERT.PUB.VOLUME is 'Volume holding the item (e.g. “2” when citing a chapter from book volume 2).'");
  op.execute("comment on column EXPERT.PUB.ISSUE is 'Issue holding the item (e.g. “5” when citing a journal article from journal volume 2, issue 5).'");
  op.execute("comment on column EXPERT.PUB.PAGES is 'Range of pages the item (e.g. a journal article) covers in a container (e.g. a journal issue).'");
  op.execute("comment on column EXPERT.PUB.CITATION_TOTAL is 'Number of citations of the item.'");

def downgrade():
  op.execute("comment on column EXPERT.PUB.PURE_UUID is NULL");
  op.execute("comment on column EXPERT.PUB.OWNER_PURE_ORG_UUID is NULL");
  op.execute("comment on column EXPERT.PUB.SCOPUS_ID is NULL");
  op.execute("comment on column EXPERT.PUB.PMID is NULL");
  op.execute("comment on column EXPERT.PUB.DOI is NULL");
  op.execute("comment on column EXPERT.PUB.TYPE is NULL");
  op.execute("comment on column EXPERT.PUB.ISSUED is NULL");
  op.execute("comment on column EXPERT.PUB.ISSUED_PRECISION is NULL");
  op.execute("comment on column EXPERT.PUB.TITLE is NULL");
  op.execute("comment on column EXPERT.PUB.CONTAINER_TITLE is NULL");
  op.execute("comment on column EXPERT.PUB.ISSN is NULL");
  op.execute("comment on column EXPERT.PUB.VOLUME is NULL");
  op.execute("comment on column EXPERT.PUB.ISSUE is NULL");
  op.execute("comment on column EXPERT.PUB.PAGES is NULL");
  op.execute("comment on column EXPERT.PUB.CITATION_TOTAL is NULL");
