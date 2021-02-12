from sqlalchemy import Table, Column, Boolean, DateTime, Integer, String, Text, create_engine, func, ForeignKey, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, relationship
from sqlalchemy_mptt.mixins import BaseNestedSets
import json

from . import db

engine = db.engine('hotel')

from . import common
Base = declarative_base(metadata=common.metadata)

class PureJsonCollectionMeta(Base):
  __tablename__ = 'pure_json_collection_meta'
  __table_args__ = {'comment': 'Maps Pure API collection names, family system names, and versions to local table names.'}
  api_name = Column(
      String(255),
      primary_key=True,
      comment='Name of the collection in the Pure API, i.e., in URL endpoints.',
  )
  api_version = Column(
      String(15),
      primary_key=True,
      comment='The Pure API version, without the decimal point, i.e., 516 for version 5.16.',
  )
  family_system_name = Column(
      String(255),
      primary_key=True,
      comment='Name of the collection in API change records, where it is called familySystemName.',
  )
  local_name = Column(
      String(255),
      primary_key=True,
      comment='Name of the collection as it appears in local table names.',
  )

class SodaMetadata:
    uuid = Column(String(36), primary_key=True)
    inserted = Column(DateTime, default=func.current_timestamp(), nullable=False)

class SodaDocument:
    json_document = Column(Text, nullable=False)
    @declared_attr
    def __table_args__(cls):
        return (CheckConstraint('json_document IS JSON', name='json_document'),)

class PureJson(SodaMetadata, SodaDocument):
    updated = Column(DateTime, default=func.current_timestamp(), nullable=False)
    pure_created = Column(DateTime(), nullable=False)
    pure_modified = Column(DateTime(), nullable=False)

class PureJsonResearchOutput516(Base, PureJson):
    __tablename__ = 'pure_json_research_output_516'

class PureJsonResearchOutput516Staging(Base, PureJson):
    __tablename__ = 'pure_json_research_output_516_staging'

class PureJsonPerson516(Base, PureJson):
    __tablename__ = 'pure_json_person_516'

class PureJsonPerson516Staging(Base, PureJson):
    __tablename__ = 'pure_json_person_516_staging'

class PureJsonExternalPerson516(Base, PureJson):
    __tablename__ = 'pure_json_external_person_516'

class PureJsonExternalPerson516Staging(Base, PureJson):
    __tablename__ = 'pure_json_external_person_516_staging'

class PureJsonOrganisation516(Base, PureJson):
    __tablename__ = 'pure_json_organisation_516'

class PureJsonOrganisation516Staging(Base, PureJson):
    __tablename__ = 'pure_json_organisation_516_staging'

class PureJsonExternalOrganisation516(Base, PureJson):
    __tablename__ = 'pure_json_external_organisation_516'

class PureJsonExternalOrganisation516Staging(Base, PureJson):
    __tablename__ = 'pure_json_external_organisation_516_staging'

class PureJsonResearchOutput517(Base, PureJson):
    __tablename__ = 'pure_json_research_output_517'

class PureJsonResearchOutput517Staging(Base, PureJson):
    __tablename__ = 'pure_json_research_output_517_staging'

class PureJsonPerson517(Base, PureJson):
    __tablename__ = 'pure_json_person_517'

class PureJsonPerson517Staging(Base, PureJson):
    __tablename__ = 'pure_json_person_517_staging'

class PureJsonExternalPerson517(Base, PureJson):
    __tablename__ = 'pure_json_external_person_517'

class PureJsonExternalPerson517Staging(Base, PureJson):
    __tablename__ = 'pure_json_external_person_517_staging'

class PureJsonOrganisation517(Base, PureJson):
    __tablename__ = 'pure_json_organisation_517'

class PureJsonOrganisation517Staging(Base, PureJson):
    __tablename__ = 'pure_json_organisation_517_staging'

class PureJsonExternalOrganisation517(Base, PureJson):
    __tablename__ = 'pure_json_external_organisation_517'

class PureJsonExternalOrganisation517Staging(Base, PureJson):
    __tablename__ = 'pure_json_external_organisation_517_staging'

class PureJsonChangeCommon(SodaMetadata):
    family_system_name = Column(String(150), nullable=False)
    change_type = Column(String(10), nullable=False)
    pure_version = Column(Integer, nullable=False, primary_key=True)

class PureJsonChange(PureJsonChangeCommon, SodaDocument):
    pass

class PureJsonChangeHistory(PureJsonChangeCommon):
    pass

class PureJsonChange516(Base, PureJsonChange):
    __tablename__ = 'pure_json_change_516'

class PureJsonChange516History(Base, PureJsonChangeHistory):
    __tablename__ = 'pure_json_change_516_history'

class PureJsonChange517(Base, PureJsonChange):
    __tablename__ = 'pure_json_change_517'

class PureJsonChange517History(Base, PureJsonChangeHistory):
    __tablename__ = 'pure_json_change_517_history'

# Would like to use a longer name, like "research_output", but
# Oracle's stupid 30-character limit for names makes that difficult.
# pub is short for publication, even though not all research
# outputs are publications.
class Pub(Base):
  __tablename__ = 'pub'
  __table_args__ = {'comment': 'Research output. Named "pub", short for "publication", due to Oracle character-length limits.'}
  uuid = Column(
      String(36),
      primary_key=True,
      comment='Universally-unique ID for the item, generated for this Experts@Minnesota database.',
  )
  pure_uuid = Column(
      String(36),
      nullable=False,
      unique=True,
      index=True,
      comment='Universally-unique ID for the item in our [Elsevier Pure database](https://experts.umn.edu).',
  )
  owner_pure_org_uuid = Column(
      ForeignKey('pure_org.pure_uuid'),
      nullable=False,
      comment='Unique ID for the organization that owns the item in our [Elsevier Pure database](https://experts.umn.edu).',
  )

  # The Pure API does not provide scopus ID to us. Can we change that?
  scopus_id = Column(
      String(35),
      nullable=True,
      comment='Unique ID for the item in the [Elsevier Scopus database](https://www.elsevier.com/solutions/scopus).',
  )

  pmid = Column(
      String(50),
      nullable=True,
      comment='Unique ID for the item in the [NCBI PubMed database](https://www.ncbi.nlm.nih.gov/pubmed/).',
  )
  doi = Column(
      String(150),
      nullable=True,
      comment='[Digital Object Identifier](https://www.doi.org/) for the item.',
  )
  type = Column(
      String(50),
      nullable=True,
      comment='Publication type or format of the item. See the [CSL spec](http://docs.citationstyles.org/en/stable/specification.html#appendix-iii-types) for a list of values.',
  )
  issued = Column(
      DateTime,
      nullable=True,
      comment='Date the item was/will be issued/published.',
  )
  issued_current = Column(
      Boolean(name='issued_current_bool'),
      nullable=True,
      comment='True or false depending on whether this is a current state.',
  )
  issued_precision = Column(
      Integer,
      nullable=True,
      comment='Precision of the ISSUED column, in days: 366 (year), 31 (month), 1 (day).',
  )
  eissued = Column(
      DateTime,
      nullable=True,
      comment='Date the item was/will be electronically issued/published, possibly ahead of print.',
  )
  eissued_current = Column(
      Boolean(name='eissued_current_bool'),
      nullable=True,
      comment='True or false depending on whether this is a current state.',
  )
  eissued_precision = Column(
      Integer,
      nullable=True,
      comment='Precision of the EISSUED column, in days: 366 (year), 31 (month), 1 (day).',
  )
  unissued = Column(
      DateTime,
      nullable=True,
      comment='Date the item was/will be unissued/unpublished.',
  )
  unissued_current = Column(
      Boolean(name='unissued_current_bool'),
      nullable=True,
      comment='True or false depending on whether this is a current state.',
  )
  unissued_precision = Column(
      Integer,
      nullable=True,
      comment='Precision of the UNISSUED column, in days: 366 (year), 31 (month), 1 (day).',
  )
  inprep = Column(
      DateTime,
      nullable=True,
      comment='Date the item was/will be in preparation to be issued/published.',
  )
  inprep_current = Column(
      Boolean(name='inprep_current_bool'),
      nullable=True,
      comment='True or false depending on whether this is a current state.',
  )
  inprep_precision = Column(
      Integer,
      nullable=True,
      comment='Precision of the INPREP column, in days: 366 (year), 31 (month), 1 (day).',
  )
  submitted = Column(
      DateTime,
      nullable=True,
      comment='Date the item was/will be submitted to be issued/published.',
  )
  submitted_current = Column(
      Boolean(name='submitted_current_bool'),
      nullable=True,
      comment='True or false depending on whether this is a current state.',
  )
  submitted_precision = Column(
      Integer,
      nullable=True,
      comment='Precision of the SUBMITTED column, in days: 366 (year), 31 (month), 1 (day).',
  )
  inpress = Column(
      DateTime,
      nullable=True,
      comment='Date the item was/will be accepted/in press.',
  )
  inpress_current = Column(
      Boolean(name='inpress_current_bool'),
      nullable=True,
      comment='True or false depending on whether this is a current state.',
  )
  inpress_precision = Column(
      Integer,
      nullable=True,
      comment='Precision of the INPRESS column, in days: 366 (year), 31 (month), 1 (day).',
  )
  title = Column(
      String(2000),
      nullable=False,
      comment='Primary title of the item.',
  )
  container_title = Column(
      String(2000),
      nullable=True,
      comment='Title of the container holding the item (e.g. the book title for a book chapter, the journal title for a journal article).',
  )
  issn = Column(
      String(9),
      nullable=True,
      comment='[International Standard Serial Number](http://www.issn.org/understanding-the-issn/what-is-an-issn/).',
  )
  volume = Column(
      String(2000),
      nullable=True,
      comment='Volume holding the item (e.g. “2” when citing a chapter from book volume 2).',
  )
  issue = Column(
      String(2000),
      nullable=True,
      comment='Issue holding the item (e.g. “5” when citing a journal article from journal volume 2, issue 5).',
  )
  pages = Column(
      String(100),
      nullable=True,
      comment='Range of pages the item (e.g. a journal article) covers in a container (e.g. a journal issue).',
  )
  citation_total = Column(
      Integer,
      nullable=True,
      comment='Number of citations of the item. We call it a "total" because Pure also provides citation counts per year, which we may decide to use later.',
  )
  pure_modified = Column(
      DateTime,
      nullable=True,
      comment='Date the associated record was last modified in Pure.',
  )

  pure_type = Column(
      String(50),
      nullable=True,
      comment='Publication type or format of the item in Pure.',
  )
  pure_subtype = Column(
      String(50),
      nullable=True,
      comment='Publication subtype or sub-format of the item in Pure.',
  )

  persons = association_proxy(
    'person_associations',
    'person',
  )
  author_collaborations = association_proxy(
    'author_collaboration_associations',
    'author_collaboration',
  )

  owner_pure_org = relationship('PureOrg', backref='publications')

  def __repr__(self):
    d = {}
    for k in ['uuid','pure_uuid','owner_pure_org_uuid','scopus_id','pmid','doi','type','issued_precision','title','container_title','issn','volume','issue','pages','citation_total']:
      d[k] = getattr(self, k)
    #return 'uuid: {}'.format(self.uuid)
    return json.dumps(d)

class PubPerson(Base):
  __tablename__ = 'pub_person'
  __table_args__ = {'comment': 'Associates research outputs with persons (authors).'}
  pub_uuid = Column(
      ForeignKey('pub.uuid'),
      nullable=False,
      primary_key=True,
      comment='Foreign key to PUB.',
  )
  person_uuid = Column(
      ForeignKey('person.uuid'),
      nullable=False,
      primary_key=True,
      comment='Foreign key to PERSON.',
  )
  emplid = Column(
      String(11),
      nullable=True,
      comment='De-normalization column. See the description in PERSON.',
  )

  # TODO: Is this the same as the publication author list?
  person_ordinal = Column(
      Integer,
      nullable=False,
      comment='The position of the person in the author list for the research output in Pure.',
  )

  first_name = Column(
      String(1024),
      nullable=True,
      comment='The given name for the person as it appears in the author list for the research output in Pure. Note that this may be differ from PERSON.FIRST_NAME.',
  )
  last_name = Column(
      String(1024),
      nullable=True,
      comment='The family name for the person as it appears in the author list for the research output in Pure. Note that this may be differ from PERSON.LAST_NAME.',
  )

  # TODO: Should the role really be nullable?
  person_role = Column(
      String(255),
      nullable=True,
      comment='"author" or "editor". Need to find Pure documentation on any other possible values.',
  )

  # TODO: Does this reflect the person's current internal/external
  # status, or the status at the time of publication?
  person_pure_internal = Column(
      String(1),
      nullable=True,
      comment='"Y" if Pure classified the person as UMN-internal at the time of publication of the research output, "N" otherwise. Note that, because we have not loaded data for all UMN persons into Pure, some UMN persons will be classified as external in Pure.',
  )

  person = relationship('Person', backref="pub_associations")
  pub = relationship('Pub', backref="person_associations")

  def __repr__(self):
    d = {}
    for k in ['pub_uuid','person_uuid','person_ordinal','person_role','person_pure_internal','first_name','last_name','emplid']:
      d[k] = getattr(self, k)
    return json.dumps(d)

class PubAuthorCollaboration(Base):
  __tablename__ = 'pub_author_collaboration'
  __table_args__ = {'comment': 'Associates research outputs with author collaborations (a type of author).'}
  pub_uuid = Column(
      ForeignKey('pub.uuid'),
      nullable=False,
      primary_key=True,
      comment='Foreign key to PUB.',
  )
  author_collaboration_uuid = Column(
      ForeignKey('author_collaboration.uuid'),
      nullable=False,
      primary_key=True,
      comment='Foreign key to AUTHOR_COLLABORATION.',
  )
  author_ordinal = Column(
      Integer,
      nullable=False,
      comment='The position of the author collaboration in the author list for the research output in Pure.',
  )
  # TODO: Should the role really be nullable?
  author_role = Column(
      String(255),
      nullable=True,
      comment='"author" or "editor". Need to find Pure documentation on any other possible values.',
  )

  author_collaboration = relationship('AuthorCollaboration', backref="pub_associations")
  pub = relationship('Pub', backref="author_collaboration_associations")

  def __repr__(self):
    d = {}
    for k in ['pub_uuid','author_collaboration_uuid','author_ordinal','author_role',]:
      d[k] = getattr(self, k)
    return json.dumps(d)


# This may need some improvement, maybe even drastic changes. Therefore, holding
# off on defining relationships for now.
# Also, does the Pure API return more than one organisation
# per person per pub? For external persons, at least, it seems to return only one.
class PubPersonPureOrg(Base):
  __tablename__ = 'pub_person_pure_org'
  __table_args__ = {'comment': 'Associates with persons with their organization affiliations at the time of publication of a research output.'}
  pub_uuid = Column(
      ForeignKey('pub.uuid'),
      nullable=False,
      primary_key=True,
      comment='Foreign key to PUB.',
  )
  person_uuid = Column(
      ForeignKey('person.uuid'),
      nullable=False,
      primary_key=True,
      comment='Foreign key to PERSON.',
  )
  pure_org_uuid = Column(
      ForeignKey('pure_org.pure_uuid'),
      nullable=False,
      primary_key=True,
      comment='Foreign key to PURE_ORG.',
  )

  def __repr__(self):
    d = {}
    for k in ['pub_uuid','person_uuid','pure_org_uuid']:
      d[k] = getattr(self, k)
    return json.dumps(d)

class Person(Base):
  __tablename__ = 'person'
  __table_args__ = {'comment': 'A person, usually an author of research outputs. May be internal or external to UMN.'}
  uuid = Column(
      String(36),
      primary_key=True,
      comment='Universally-unique ID for the person, generated for this Experts@Minnesota database.',
  )
  pure_uuid = Column(
      String(36),
      nullable=True,
      index=True,
      comment='Universally-unique ID for the person in our [Elsevier Pure database](https://experts.umn.edu).',
  )

  # May be emplid or old scival_id. Seems emplids may contain more
  # characters than scival ids, so using the emplid length:
  pure_id = Column(
      String(1024),
      nullable=True,
      index=True,
      comment='Unique ID for the person in our [Elsevier Pure database](https://experts.umn.edu). For UMN persons whose data we loaded into the Elsevier predecessor product, SciVal, this will be the SciVal ID. For other UMN persons whose data we have loaded into Pure, this will be the UMN employee ID (emplid). For UMN-external persons, this will be NULL. Note that because we have not loaded data for all UMN persons into Pure, some UMN persons will be classified as external in Pure.',
  )

  # Not sure where to get this. Pure API research outputs? Scopus?
  # It's not in the Pure API person data.
  orcid = Column(
      String(20),
      nullable=True,
      comment='[Open Researcher and Contributor ID](https://orcid.org/) for the person.',
  )

  # This scopus ID may be unnecessarily long. Also, some sources claim
  # that a person may (incorrectly, I think) have more than one scopus ID:
  scopus_id = Column(
      String(35),
      nullable=True,
      comment='Unique ID for the person in the [Elsevier Scopus database](https://www.elsevier.com/solutions/scopus).',
  )

  # Apparently there can be multiples of these, from different sources.
  # We use only the one from Scopus for now:
  hindex = Column(
      Integer,
      nullable=True,
      comment='An index that attempts to measure both the productivity and impact of the published work of a scientist or scholar. Used only in some disciplines, so for many persons this will be NULL. [More info](https://blog.scopus.com/posts/the-scopus-h-index-what-s-it-all-about-part-i) on [blog.scopus.com](https://blog.scopus.com/posts/5-facts-about-scopus-and-the-h-index).',
  )

  emplid = Column(
      String(11),
      nullable=True,
      index=True,
      comment='UMN employee ID (emplid).',
  )
  internet_id = Column(
      String(15),
      nullable=True,
      comment='UMN internet ID.',
  )
  first_name = Column(
      String(1024),
      nullable=True,
      comment='The given name for the person.',
  )
  last_name = Column(
      String(1024),
      nullable=True,
      comment='The family name for the person.',
  )
  pure_internal = Column(
      String(1),
      nullable=False,
      comment='"Y" if Pure classifies the person as UMN-internal, "N" otherwise. Note that, because we have not loaded data for all UMN persons into Pure, some UMN persons will be classified as external in Pure.',
  )

  # Date the associated record was last modified in Pure.
  pure_modified = Column(DateTime, nullable=True)

  # Reads from and writes to a list of PersonScopusId objects:
  _scopus_ids = relationship('PersonScopusId', backref='person')

  # Provides a 'view' of PersonScopusId objects as a list of scopus_id strings.
  scopus_ids = association_proxy(
    '_scopus_ids',
    'scopus_id',
  )

  publications = association_proxy(
    'pub_associations',
    'pub',
  )

  pure_orgs = association_proxy(
    'pure_org_associations',
    'pure_org',
  )

  umn_pure_orgs = association_proxy(
    'umn_pure_org_associations',
    'pure_org',
  )

  def __repr__(self):
    d = {}
    for k in ['uuid','pure_uuid','pure_id','orcid','hindex','emplid','internet_id','first_name','last_name','pure_internal']:
      d[k] = getattr(self, k)
    #return 'uuid: {}'.format(self.uuid)
    return json.dumps(d)

class AuthorCollaboration(Base):
  __tablename__ = 'author_collaboration'
  __table_args__ = {'comment': 'An organization through which authors collaborate on research outputs.'}
  uuid = Column(
      String(36),
      primary_key=True,
      comment='Universally-unique ID for the author collaboration, generated for this Experts@Minnesota database.',
  )
  pure_uuid = Column(
      String(36),
      nullable=False,
      index=True,
      comment='Universally-unique ID for the author collaboration in our [Elsevier Pure database](https://experts.umn.edu).',
  )
  name = Column(
      String(1024),
      nullable=False,
      comment='The name of the author collaboration organization.',
  )

  publications = association_proxy(
    'pub_associations',
    'pub',
  )

  def __repr__(self):
    d = {}
    for k in ['uuid','pure_uuid','name',]:
      d[k] = getattr(self, k)
    return json.dumps(d)

class PersonScopusId(Base):
  __tablename__ = 'person_scopus_id'
  person_uuid = Column(ForeignKey('person.uuid'), primary_key=True)

  # This scopus ID may be unnecessarily long:
  scopus_id = Column(String(35), primary_key=True)

  def __repr__(self):
    return 'person_uuid: {}, scopus_id: {}'.format(self.person_uuid, self.scopus_id)

# The hierarchy of Pure UMN-internal organisations.
# Not all Pure organisations are UMN-internal.
# External orgs are not included here.
class PureInternalOrg(Base, BaseNestedSets):
  __tablename__ = 'pure_internal_org'
  __table_args__ = {'comment': 'The hierarchy (tree) of Pure UMN-internal organizations. This tree uses [nested sets](https://en.wikipedia.org/wiki/Nested_set_model), as implemented by the Python package [sqlalchemy_mptt](https://pypi.python.org/pypi/sqlalchemy_mptt/). However, because Oracle supports [recursive queries](https://explainextended.com/2009/09/28/adjacency-list-vs-nested-sets-oracle/), this may not be the best implementation. Because parent-child relationships (adjacency lists) already exist in the PURE_ORG table, this entire table may be unnecessary and may go away.'}
  id = Column(
      Integer,
      primary_key=True,
      comment='The unique ID for the node. Defined by sqlalchemy_mptt.',
  )
  pure_uuid = Column(
      ForeignKey('pure_org.pure_uuid'),
      nullable=False,
      comment='See the description in PURE_ORG.',
  )

  # De-normalization columns--not really required:
  pure_id = Column(
      String(1024),
      nullable=True,
      index=True,
      comment='See the description in PURE_ORG.',
  )
  name_en = Column(
      String(512),
      comment='See the description in PURE_ORG.',
  )

  pure_org = relationship('PureOrg', backref=backref('pure_internal_org', uselist=False))

  def __repr__(self):
    #return 'id: {}, parent_id: {}, lft: {}, rgt: {}, pure_uuid: {}, name_en: {}'.format(self.id, self.parent_id, self.lft, self.rgt, self.pure_uuid, self.name_en)
    return 'id: {}, pure_uuid: {}, pure_id: {}, name_en: {}'.format(self.id, self.pure_uuid, self.pure_id, self.name_en)

class PureOrg(Base):
  __tablename__ = 'pure_org'
  __table_args__ = {'comment': 'An organization (e.g. university, college, department, etc.) in Pure. May be internal or external to UMN. Pure requires all UMN-internal organizations to be part of a single hierarchy, with UMN itself as the root. Note that sometimes we combine multiple UMN departments into one Pure organization. UMN-external organizations are never part of a hierarchy in Pure, and Pure gives us limited information for them in general.'}
  pure_uuid = Column(
      String(36),
      primary_key=True,
      comment='Universally-unique ID for the organization in our [Elsevier Pure database](https://experts.umn.edu).',
  )
  pure_id = Column(
      String(1024),
      nullable=True,
      comment='Unique ID for the organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations, and some UMN-internal organizations.',
  )
  parent_pure_uuid = Column(
      String(36),
      nullable=True,
      comment='Universally-unique ID for the parent organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations.',
  )
  parent_pure_id = Column(
      String(1024),
      nullable=True,
      comment='Unique ID for the parent organization in our [Elsevier Pure database](https://experts.umn.edu). NULL for UMN-external organizations, and some UMN-internal organizations.',
  )
  pure_internal = Column(
      String(1),
      nullable=False,
      comment='"Y" if Pure classifies the organization as UMN-internal, "N" otherwise.',
  )
  type = Column(
      String(1024),
      nullable=True,
      comment='"academic", "college", "corporate", "department", "government", "initiative", "institute", "medical", "private non-profit", "university", or "unknown"',
  )
  name_en = Column(
      String(512),
      nullable=False,
      comment='Name of the organization. Called "name_en" to be consistent with Pure naming, and to indicate that this is an English name.',
  )
  name_variant_en = Column(
      String(1024),
      nullable=True,
      comment='An alternative name of the organization. Called "name_variant_en" to be consistent with Pure naming, and to indicate that this is an English name.',
  )
  url = Column(
      String(1024),
      nullable=True,
      comment='The website for the organization.',
  )
  pure_modified = Column(
      DateTime,
      nullable=True,
      comment='Date the associated record was last modified in Pure.',
  )

  persons = association_proxy(
    'person_associations',
    'person',
  )

  umn_persons = association_proxy(
    'umn_person_associations',
    'person',
  )

  umn_depts = relationship('UmnDeptPureOrg', backref='pure_org')

  def __repr__(self):
    return 'pure_uuid: {}, pure_id: {}, type: {}, name_en: {}'.format(self.pure_uuid, self.pure_id, self.type, self.name_en)

class PersonPureOrg(Base):
  __tablename__ = 'person_pure_org'
  __table_args__ = {'comment': 'Associates persons with their organizations.'}
  person_uuid = Column(
      ForeignKey('person.uuid'),
      nullable=False,
      primary_key=True,
      comment='Foreign key to PERSON.',
  )
  pure_org_uuid = Column(
      ForeignKey('pure_org.pure_uuid'),
      nullable=False,
      primary_key=True,
      comment='Foreign key to PURE_ORG.',
  )

  person = relationship('Person', backref="pure_org_associations")
  pure_org = relationship('PureOrg', backref="person_associations")

  def __repr__(self):
    return 'person_uuid: {}, pure_org_uuid: {}'.format(self.pub_uuid, self.person_uuid, self.pure_org_uuid)

# We need this table, in addition to person_pure_org, because we get far more data
# for UMN-internal persons, some of which we use to ensure row uniqueness.
class UmnPersonPureOrg(Base):
  __tablename__ = 'umn_person_pure_org'
  __table_args__ = {'comment': 'Associates persons that Pure classifies as UMN-internal with Pure organizations. We use this table, in addition to PERSON_PURE_ORG, because Pure attaches far more data to UMN-internal persons, some of which we use to ensure row uniqueness. Note that there are four columns in the primary key: PURE_ORG_UUID, PERSON_UUID, JOB_DESCRIPTION, and START_DATE. This is because UMN-internal persons may change positions, and also organization affiliations, over time. There may be multiple rows for the same person in this table.'}
  person_uuid = Column(
      ForeignKey('person.uuid'),
      nullable=False,
      primary_key=True,
      comment='Foreign key to PERSON.',
  )
  pure_org_uuid = Column(
      ForeignKey('pure_org.pure_uuid'),
      nullable=False,
      primary_key=True,
      comment='Foreign key to PURE_ORG.',
  )

  # De-normalization columns--not really required.
  emplid = Column(
      String(11),
      nullable=False,
      comment='De-normalization column. See the description in PERSON.',
  )
  pure_person_id = Column(
      String(11),
      nullable=False,
      comment='De-normalization column. See the description for PERSON.PURE_ID.',
  )
  pure_org_id = Column(
      String(1024),
      nullable=True,
      comment='De-normalization column. See the description for PURE_ORG.PURE_ID.',
  )

  # We should probably include a job code in the PK instead of this, but we
  # don't have those yet:
  job_description = Column(
      String(1024),
      nullable=True,
      primary_key=True,
      comment='The description of this job in PeopleSoft. Maybe be better to use a job code here instead.',
  )

  employed_as = Column(
      String(1024),
      nullable=True,
      comment='Always "Academic" for the data we have loaded so far. Uncertain whether we will have other values in the future.',
  )
  staff_type = Column(
      String(1024),
      nullable=True,
      comment='"academic" or "nonacademic".',
  ) # (non)?academic

  # Seems wrong that we should have to add this to the PK, but it's the only
  # way I can get the data to load the first time, at least:
  start_date = Column(
      DateTime,
      default=func.current_timestamp(),
      primary_key=True,
      comment='The date the person started this job with this organization.',
  )

  end_date = Column(
      DateTime,
      nullable=True,
      comment='The date the person ended this job with this organization.',
  )
  primary = Column(
      String(1),
      nullable=True,
      comment='"Y" if this is the person"s primary organization affiliation, otherwise "N".',
  )

  person = relationship('Person', backref="umn_pure_org_associations")
  pure_org = relationship('PureOrg', backref="umn_person_associations")

class UmnDeptPureOrg(Base):
  __tablename__ = 'umn_dept_pure_org'
  __table_args__ = {'comment': 'Associates UMN departments with Pure organizations. Note that many UMN departments may map to one Pure organization.'}
  deptid = Column(String(10), primary_key=True)
  deptid_descr = Column(
      String(255),
      nullable=True,
      comment='Name of the UMN department in PeopleSoft. De-normalization column.',
  )
  pure_org_uuid = Column(ForeignKey('pure_org.pure_uuid'), nullable=False)
  pure_org_id = Column(
      String(1024),
      nullable=False,
      comment='Unique ID for the organization in our [Elsevier Pure database](https://experts.umn.edu).',
  )

  def __repr__(self):
    return 'umn_dept_id: {}, umn_dept_name: {}, pure_org_uuid: {}, pure_org_id: {}'.format(self.umn_dept_id, self.umn_dept_name, self.pure_org_uuid, self.pure_org_id)

class PureEligibleEmployeeJobcode(Base):
  __tablename__ = 'pure_eligible_employee_jobcode'
  jobcode = Column(String(13), primary_key=True)
  jobcode_descr = Column(String(35), nullable=True)
  pure_job_description = Column(String(50), nullable=False)
  default_employed_as = Column(String(50), nullable=False)
  default_staff_type = Column(String(11), nullable=False)
  default_visibility = Column(String(10), nullable=False)
  default_profiled = Column(Boolean(name='default_profiled_bool'), nullable=False)
  default_profiled_overrideable = Column(Boolean(name='default_profiled_overrideable_bool'), nullable=False)

class PureEligibleAffiliateJobcode(Base):
  __tablename__ = 'pure_eligible_affiliate_jobcode'
  jobcode = Column(String(13), primary_key=True)
  jobcode_descr = Column(String(35), nullable=True)
  pure_job_description = Column(String(50), nullable=False)
  default_employed_as = Column(String(50), nullable=False)
  default_staff_type = Column(String(11), nullable=False)
  default_visibility = Column(String(10), nullable=False)
  default_profiled = Column(Boolean(name='default_profiled_bool'), nullable=False)

class PureEligiblePOIJobcode(Base):
  __tablename__ = 'pure_eligible_poi_jobcode'
  jobcode = Column(String(13), primary_key=True)
  jobcode_descr = Column(String(35), nullable=True)
  pure_job_description = Column(String(50), nullable=False)
  default_employed_as = Column(String(50), nullable=False)
  default_staff_type = Column(String(11), nullable=False)
  default_visibility = Column(String(10), nullable=False)
  default_profiled = Column(Boolean(name='default_profiled_bool'), nullable=False)

class PureEligibleAffiliateDept(Base):
  __tablename__ = 'pure_eligible_affiliate_dept'
  deptid = Column(String(10), primary_key=True)

class PureEmployeeJobcodeDefaultOverride(Base):
  __tablename__ = 'pure_employee_jobcode_default_override'
  jobcode = Column(String(13), primary_key=True)
  deptid = Column(String(10), primary_key=True)
  profiled = Column(Boolean(name='profiled_bool'), nullable=False)

class KnownOverrideableEmployeeJobcodeDept(Base):
  __tablename__ = 'known_overrideable_employee_jobcode_dept'
  jobcode = Column(String(13), primary_key=True)
  deptid = Column(String(10), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)

class UmnDataError(Base):
  __tablename__ = 'umn_data_error'
  error_id = Column(String(40), primary_key=True)
  message = Column(String(255), nullable=False)
  jobcode = Column(String(13), nullable=True)
  jobcode_descr = Column(String(35), nullable=True)
  deptid = Column(String(10), nullable=True)
  deptid_descr = Column(String(30), nullable=True)
  persons_in_dept = Column(Integer, nullable=True)
  um_college = Column(String(10), nullable=True)
  um_college_descr = Column(String(30), nullable=True)
  um_campus = Column(String(10), nullable=True)
  um_campus_descr = Column(String(30), nullable=True)
  emplid = Column(String(11), nullable=True)
  internet_id = Column(String(15), nullable=True)
  first_seen = Column(DateTime, default=func.current_timestamp(), nullable=False)
  last_seen = Column(DateTime, default=func.current_timestamp(), nullable=False)
  count = Column(Integer, nullable=False)
  # If null, the error has not been reported, i.e, no notification has been sent.
  reported = Column(DateTime, nullable=True)
  notes = Column(Text, nullable=True)

  def __repr__(self):
    return self.message

## Pure sync tables, for populating XML files to upload to Pure.

# Based on PERSON_DATA in:
# https://doc.pure.elsevier.com/download/attachments/28412327/oracle_person_view_create_statements.sql?version=5&modificationDate=1529322570793&api=v2
class PureSyncPersonData(Base):
  __tablename__ = 'pure_sync_person_data'
  person_id = Column(String(1024), primary_key=True)
  first_name = Column(String(1024), nullable=True)
  last_name = Column(String(1024), nullable=False)
  # Pure allows the remaining columns to be null, but UMN does not:
  visibility = Column(String(1024), nullable=False) # 'Public', 'Campus', or 'Restricted'
  profiled = Column(Boolean(name='profiled_bool'), nullable=False)
  #profiled = Column(Boolean(), nullable=False)

  # Added by UMN:
  emplid = Column(String(11), nullable=False)
  internet_id = Column(String(15), nullable=True)
  # We use this instead of the Pure PERSON_TITLES table, because this is the only title we use:
  postnominal = Column(String(255), nullable=True)
  created = Column(DateTime, nullable=True)
  modified = Column(DateTime, nullable=True)

  staff_org_associations = relationship('PureSyncStaffOrgAssociation', backref='person')
  user = relationship('PureSyncUserData', backref='person')

  # Unused columns from Pure's PERSON_DATA spec.
#  date_of_birth = Column(DateTime, nullable=True)
#  nationality = Column(String(1024), nullable=True)
#  gender = Column(String(1024) nullable=True) # We always set this to 'unknown'.
#  employee_start_date = Column(DateTime, nullable=True)
#  system_leaving_date = Column(DateTime, nullable=True)
#  retiral_date = Column(DateTime, nullable=True)
#  academic_profession_entry = Column(DateTime, nullable=True)
#  expert = Column(Boolean(), nullable=True)
#  willingness_to_phd  = Column(Boolean(), nullable=True)
#  phd_research_projects = CLOB,
#  affiliation_note = CLOB,
#  orcid = Column(String(20), nullable=True)
#  building = Column(String(1024), nullable=True)
#  city = Column(String(1024), nullable=True)
#  country = Column(String(1024), nullable=True)
#  postal_code = Column(String(1024), nullable=True)
#  road = Column(String(1024), nullable=True)
#  room = Column(String(1024), nullable=True)
#  user_id = Column(String(1024), nullable=True)
#  managed_in_pure = Column(Boolean(), nullable=True) # We always set this to 'false'.

class PureSyncPersonDataScratch(Base):
  __tablename__ = 'pure_sync_person_data_scratch'
  __table_args__ = {'comment': 'Scratch table for pure_sync_person_data.'}
  person_id = Column(String(1024), primary_key=True)
  first_name = Column(String(1024), nullable=True)
  last_name = Column(String(1024), nullable=False)
  visibility = Column(String(1024), nullable=False)
  profiled = Column(Boolean(name='profiled_bool'), nullable=False)
  #profiled = Column(Boolean(), nullable=False)
  emplid = Column(String(11), nullable=False)
  internet_id = Column(String(15), nullable=True)
  postnominal = Column(String(255), nullable=True)

  staff_org_associations = relationship('PureSyncStaffOrgAssociationScratch', backref='person')
  user = relationship('PureSyncUserDataScratch', backref='person')

# Based on STAFF_ORG_RELATION in:
# https://doc.pure.elsevier.com/download/attachments/28412327/oracle_person_view_create_statements.sql?version=5&modificationDate=1529322570793&api=v2
class PureSyncStaffOrgAssociation(Base):
  __tablename__ = 'pure_sync_staff_org_association'
  staff_org_association_id = Column(String(1024), primary_key=True)
  person_id = Column(ForeignKey('pure_sync_person_data.person_id'), nullable=False)
  period_start_date = Column(DateTime, nullable=False)
  period_end_date = Column(DateTime, nullable=True)
  # Pure allows the remaining columns to be null, but UMN does not:
  org_id = Column(String(1024), nullable=False)
  employment_type = Column(String(1024), nullable=False)
  staff_type = Column(String(1024), nullable=False) # 'academic' or 'nonacademic'
  visibility = Column(String(1024), nullable=False) # 'Public', 'Campus', or 'Restricted'
  primary_association = Column(Boolean(name='primary_association_bool'), nullable=False)
  #primary_association = Column(Boolean(), nullable=False)
  job_description = Column(String(1024), nullable=False)

  # Added by UMN:
  # person.xsd can include affiliationId, but there seems to be no column for it in Pure's
  # STAFF_ORG_RELATION spec. We use this for jobcode.
  affiliation_id = Column(String(30), nullable=True)
  created = Column(DateTime, nullable=True)
  modified = Column(DateTime, nullable=True)

  # Unused columns from Pure's STAFF_ORG_RELATION spec.
#  org_pure_id = Column(Integer, nullable=True)
#  org_source_id = Column(String(1024), nullable=True)
#  org_classified_ids_id = Column(String(1024), nullable=True)
#  org_classified_ids_type = Column(String(1024), nullable=True)
#  contract_type = Column(String(1024), nullable=True)
#  job_title = Column(String(1024), nullable=True)
#  fte = Column(Integer, nullable=True)
#  managed_in_pure = Column(Boolean(), nullable=True) # We always set this to 'false'.

class PureSyncStaffOrgAssociationScratch(Base):
  __tablename__ = 'pure_sync_staff_org_association_scratch'
  __table_args__ = {'comment': 'Scratch table for pure_sync_staff_org_association.'}
  staff_org_association_id = Column(String(1024), primary_key=True)
  person_id = Column(ForeignKey('pure_sync_person_data_scratch.person_id'), nullable=False)
  period_start_date = Column(DateTime, nullable=False)
  period_end_date = Column(DateTime, nullable=True)
  org_id = Column(String(1024), nullable=False)
  employment_type = Column(String(1024), nullable=False)
  staff_type = Column(String(1024), nullable=False) # 'academic' or 'nonacademic'
  visibility = Column(String(1024), nullable=False) # 'Public', 'Campus', or 'Restricted'
  primary_association = Column(Boolean(name='primary_association_bool'), nullable=False)
  #primary_association = Column(Boolean(), nullable=False)
  job_description = Column(String(1024), nullable=False)
  affiliation_id = Column(String(30), nullable=True)

# Based on:
# https://doc.pure.elsevier.com/download/attachments/28412333/oracle_user_view_create_statements.sql?version=1&modificationDate=1424698361313&api=v2
class PureSyncUserData(Base):
  __tablename__ = 'pure_sync_user_data'
  person_id = Column(ForeignKey('pure_sync_person_data.person_id'), primary_key=True) # 'id' in Pure's USER_DATA spec
  first_name = Column(String(1024), nullable=True)
  last_name = Column(String(1024), nullable=True)
  user_name = Column(String(1024), nullable=False) # umn internet id
  email = Column(String(1024), nullable=False)

  # Added by UMN:
  created = Column(DateTime, nullable=True)
  modified = Column(DateTime, nullable=True)

class PureSyncUserDataScratch(Base):
  __tablename__ = 'pure_sync_user_data_scratch'
  __table_args__ = {'comment': 'Scratch table for pure_sync_user_data.'}
  person_id = Column(ForeignKey('pure_sync_person_data_scratch.person_id'), primary_key=True) # 'id' in Pure's USER_DATA spec
  first_name = Column(String(1024), nullable=True)
  last_name = Column(String(1024), nullable=True)
  user_name = Column(String(1024), nullable=False) # umn internet id
  email = Column(String(1024), nullable=False)

## Views

class PureEligibleDemog(Base):
  __table__ = Table(
    'pure_eligible_demog',
    Base.metadata,
    Column('emplid', String(11), primary_key=True),
    autoload=True,
    autoload_with=engine
 )

class PureEligibleDemographics(Base):
  __table__ = Table(
    'pure_eligible_demographics',
    Base.metadata,
    Column('emplid', String(11), primary_key=True),
    autoload=True,
    autoload_with=engine
 )

class PureEligiblePerson(Base):
  __table__ = Table(
    'pure_eligible_person',
    Base.metadata,
    Column('emplid', String(11), primary_key=True),
    autoload=True,
    autoload_with=engine
 )

class PureEligibleEmployeeJob(Base):
  __table__ = Table(
    'pure_eligible_employee_job',
    Base.metadata,
    Column('emplid', String(11), primary_key=True),
    Column('position_nbr', String(8), primary_key=True),
    Column('effdt', DateTime, primary_key=True),
    Column('effseq', Integer, primary_key=True),
    autoload=True,
    autoload_with=engine
 )

class PureEligibleAffiliateJob(Base):
  __table__ = Table(
    'pure_eligible_affiliate_job',
    Base.metadata,
    Column('emplid', String(11), primary_key=True),
    Column('um_affiliate_id', String(2), primary_key=True),
    Column('effdt', DateTime, primary_key=True),
    Column('deptid', String(10), primary_key=True),
    autoload=True,
    autoload_with=engine
 )

class PureEligiblePOIJob(Base):
  __table__ = Table(
    'pure_eligible_poi_job',
    Base.metadata,
    Column('emplid', String(11), primary_key=True),
    Column('position_nbr', String(8), primary_key=True),
    Column('effdt', DateTime, primary_key=True),
    Column('deptid', String(10), primary_key=True),
    autoload=True,
    autoload_with=engine
 )

## Snapshot tables for the views above:

class PureEligiblePersonNew(Base):
  __tablename__ = 'pure_eligible_person_new'
  emplid = Column(String(11), primary_key=True)

class PureEligiblePersonChngHst(Base):
  __tablename__ = 'pure_eligible_person_chng_hst'
  emplid = Column(String(11), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'emplid: {}, timestamp: {}'.format(self.emplid, self.timestamp)

class PureEligibleDemogNew(Base):
  __tablename__ = 'pure_eligible_demog_new'
  emplid = Column(String(11), primary_key=True)
  internet_id = Column(String(15), nullable=True)
  name = Column(String(50), nullable=True)
  last_name = Column(String(30), nullable=True)
  first_name = Column(String(30), nullable=True)
  middle_initial = Column(String(1), nullable=True)
  name_suffix = Column(String(3), nullable=True)
  instl_email_addr = Column(String(70), nullable=True)
  tenure_flag = Column(String(1), nullable=True)
  tenure_track_flag = Column(String(1), nullable=True)
  primary_empl_rcdno = Column(String(38), nullable=True)

# A history of demographics changes.
class PureEligibleDemogChngHst(Base):
  __tablename__ = 'pure_eligible_demog_chng_hst'
  emplid = Column(String(11), primary_key=True)
  internet_id = Column(String(15), nullable=True)
  name = Column(String(50), nullable=True)
  last_name = Column(String(30), nullable=True)
  first_name = Column(String(30), nullable=True)
  middle_initial = Column(String(1), nullable=True)
  name_suffix = Column(String(3), nullable=True)
  instl_email_addr = Column(String(70), nullable=True)
  tenure_flag = Column(String(1), nullable=True)
  tenure_track_flag = Column(String(1), nullable=True)
  primary_empl_rcdno = Column(String(38), nullable=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), primary_key=True)

## Tables that store records and metadata retrieved via the Pure web services API.

class PureApiChange(Base):
  __tablename__ = 'pure_api_change'
  uuid = Column(String(36), primary_key=True)
  family_system_name = Column(String(150), nullable=False)
  change_type = Column(String(10), nullable=False)
  json = Column(Text, nullable=False)
  version = Column(Integer, nullable=False, primary_key=True)
  downloaded = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'uuid: {}, family_system_name: {}, change_type: {}, version: {}, downloaded: {}'.format(self.uuid, self.family_system_name, self.change_type, self.version, self.downloaded)

class PureApiChangeHst(Base):
  __tablename__ = 'pure_api_change_hst'
  uuid = Column(String(36), primary_key=True)
  family_system_name = Column(String(150), nullable=False)
  change_type = Column(String(10), nullable=False)
  version = Column(Integer, nullable=False, primary_key=True)
  downloaded = Column(DateTime, nullable=False)
  processed = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'uuid: {}, family_system_name: {}, change_type: {}, version: {}, downloaded: {}, processed: {}'.format(self.uuid, self.family_system_name, self.change_type, self.version, self.downloaded, self.processed)

class PureApiPub(Base):
  __tablename__ = 'pure_api_pub'
  __table_args__ = (CheckConstraint('json IS JSON', name='json'),)
  uuid = Column(String(36), primary_key=True)
  json = Column(Text, nullable=False)
  modified = Column(DateTime, nullable=False, primary_key=True)
  downloaded = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'uuid: {}, modified: {}, downloaded: {}'.format(self.uuid, self.modified, self.downloaded)

class PureApiPubHst(Base):
  __tablename__ = 'pure_api_pub_hst'
  uuid = Column(String(36), primary_key=True)
  modified = Column(DateTime, nullable=False, primary_key=True)
  downloaded = Column(DateTime, nullable=False)
  processed = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'uuid: {}, modified: {}, downloaded: {}, processed: {}'.format(self.uuid, self.modified, self.downloaded, self.processed)

class PureApiInternalPerson(Base):
  __tablename__ = 'pure_api_internal_person'
  __table_args__ = (CheckConstraint('json IS JSON', name='json'),)
  uuid = Column(String(36), primary_key=True)
  json = Column(Text, nullable=False)
  modified = Column(DateTime, nullable=False, primary_key=True)
  downloaded = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'uuid: {}, modified: {}, downloaded: {}'.format(self.uuid, self.modified, self.downloaded)

class PureApiInternalPersonHst(Base):
  __tablename__ = 'pure_api_internal_person_hst'
  uuid = Column(String(36), primary_key=True)
  modified = Column(DateTime, nullable=False, primary_key=True)
  downloaded = Column(DateTime, nullable=False)
  processed = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'uuid: {}, modified: {}, downloaded: {}, processed: {}'.format(self.uuid, self.modified, self.downloaded, self.processed)

class PureApiExternalPerson(Base):
  __tablename__ = 'pure_api_external_person'
  __table_args__ = (CheckConstraint('json IS JSON', name='json'),)
  uuid = Column(String(36), primary_key=True)
  json = Column(Text, nullable=False)
  modified = Column(DateTime, nullable=False, primary_key=True)
  downloaded = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'uuid: {}, modified: {}, downloaded: {}'.format(self.uuid, self.modified, self.downloaded)

class PureApiExternalPersonHst(Base):
  __tablename__ = 'pure_api_external_person_hst'
  uuid = Column(String(36), primary_key=True)
  modified = Column(DateTime, nullable=False, primary_key=True)
  downloaded = Column(DateTime, nullable=False)
  processed = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'uuid: {}, modified: {}, downloaded: {}, processed: {}'.format(self.uuid, self.modified, self.downloaded, self.processed)

class PureApiInternalOrg(Base):
  __tablename__ = 'pure_api_internal_org'
  __table_args__ = (CheckConstraint('json IS JSON', name='json'),)
  uuid = Column(String(36), primary_key=True)
  json = Column(Text, nullable=False)
  modified = Column(DateTime, nullable=False, primary_key=True)
  downloaded = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'uuid: {}, modified: {}, downloaded: {}'.format(self.uuid, self.modified, self.downloaded)

class PureApiInternalOrgHst(Base):
  __tablename__ = 'pure_api_internal_org_hst'
  uuid = Column(String(36), primary_key=True)
  modified = Column(DateTime, nullable=False, primary_key=True)
  downloaded = Column(DateTime, nullable=False)
  processed = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'uuid: {}, modified: {}, downloaded: {}, processed: {}'.format(self.uuid, self.modified, self.downloaded, self.processed)

class PureApiExternalOrg(Base):
  __tablename__ = 'pure_api_external_org'
  __table_args__ = (CheckConstraint('json IS JSON', name='json'),)
  uuid = Column(String(36), primary_key=True)
  json = Column(Text, nullable=False)
  modified = Column(DateTime, nullable=False, primary_key=True)
  downloaded = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'uuid: {}, modified: {}, downloaded: {}'.format(self.uuid, self.modified, self.downloaded)

class PureApiExternalOrgHst(Base):
  __tablename__ = 'pure_api_external_org_hst'
  uuid = Column(String(36), primary_key=True)
  modified = Column(DateTime, nullable=False, primary_key=True)
  downloaded = Column(DateTime, nullable=False)
  processed = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'uuid: {}, modified: {}, downloaded: {}, processed: {}'.format(self.uuid, self.modified, self.downloaded, self.processed)

