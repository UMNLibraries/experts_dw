from sqlalchemy import Table, Column, DateTime, Integer, String, Text, create_engine, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, relationship
from sqlalchemy_mptt.mixins import BaseNestedSets
import json

from . import db

engine = db.engine('hotel')

# Would like to name constraints, but Oracle limits names to 30 characters!
#import common
#Base = declarative_base(metadata=common.metadata)
Base = declarative_base()

# Would like to use a longer name, like "research_output", but
# Oracle's stupid 30-character limit for names makes that difficult.
# pub is short for publication, even though not all research
# outputs are publications.
class Pub(Base):
  __tablename__ = 'pub'
  uuid = Column(String(36), primary_key=True)
  pure_uuid = Column(String(36), nullable=False, unique=True, index=True)
  owner_pure_org_uuid = Column(ForeignKey('pure_org.pure_uuid'), nullable=False)

  # The Pure API does not provide scopus ID to us. Can we change that?
  scopus_id = Column(String(35), nullable=True)

  pmid = Column(String(50), nullable=True)
  doi = Column(String(150), nullable=True)

  # See CSL spec for a list of types.
  type = Column(String(50), nullable=True)

  # Publication date: we call it "issued" to conform with CSL.
  issued = Column(DateTime, nullable=False)
  # Precision in days: 366 (year), 31 (month), 1 (day), etc. 
  # Maybe 0 could represent a timestamp?
  issued_precision = Column(Integer, nullable=False)

  title = Column(String(2000), nullable=False)
  container_title = Column(String(2000), nullable=True)
  issn = Column(String(9), nullable=True)
  volume = Column(String(25), nullable=True)
  issue = Column(String(50), nullable=True)
  pages = Column(String(50), nullable=True)

  # Total number of citations of the output. We call it a "total" because Pure
  # also provides citation counts per year, which we may decide to use later.
  citation_total = Column(Integer, nullable=True)

  # Date the associated record was last modified in Pure.
  pure_modified = Column(DateTime, nullable=True)

  persons = association_proxy(
    'person_associations',
    'person',
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
  pub_uuid = Column(ForeignKey('pub.uuid'), nullable=False, primary_key=True)
  person_uuid = Column(ForeignKey('person.uuid'), nullable=False, primary_key=True)
  emplid = Column(String(11), nullable=True)

  # Ordinal refers to the person's position in the Pure author list.
  # TODO: Is this the same as the publication author list?
  person_ordinal = Column(Integer, nullable=False)

  # Person's name as it appears in the Pure author list. 
  # TODO: Does this reflect the person's name at the time of publication,
  # such that it may be different than the current name?
  first_name = Column(String(100), nullable=True)
  last_name = Column(String(100), nullable=True)

  # TODO: Should the role really be nullable?
  person_role = Column(String(255), nullable=True)

  # (Y|N): Y if the person is included in our UMN Pure database,
  # i.e. true only if the person is/was UMN-affiliated AND we
  # have loaded that person's info into Pure.
  # TODO: Does this reflect the person's current internal/external
  # status, or the status at the time of publication?
  person_pure_internal = Column(String(1), nullable=True) 

  person = relationship('Person', backref="pub_associations")
  pub = relationship('Pub', backref="person_associations")

  def __repr__(self):
    d = {}
    for k in ['pub_uuid','person_uuid','person_ordinal','person_role','person_pure_internal','first_name','last_name','emplid']:
      d[k] = getattr(self, k)
    return json.dumps(d)

# This may need some improvement, maybe even drastic changes. Therefore, holding
# off on defining relationships for now.
# Also, does the Pure API return more than one organisation
# per person per pub? For external persons, at least, it seems to return only one.
class PubPersonPureOrg(Base):
  __tablename__ = 'pub_person_pure_org'
  pub_uuid = Column(ForeignKey('pub.uuid'), nullable=False, primary_key=True)
  person_uuid = Column(ForeignKey('person.uuid'), nullable=False, primary_key=True)
  pure_org_uuid = Column(ForeignKey('pure_org.pure_uuid'), nullable=False, primary_key=True)

  def __repr__(self):
    d = {}
    for k in ['pub_uuid','person_uuid','pure_org_uuid']:
      d[k] = getattr(self, k)
    return json.dumps(d)

class Person(Base):
  __tablename__ = 'person'
  uuid = Column(String(36), primary_key=True)
  pure_uuid = Column(String(36), nullable=True, index=True)

  # May be emplid or old scival_id. Seems emplids may contain more
  # characters than scival ids, so using the emplid length:
  pure_id = Column(String(11), nullable=True, index=True)

  # Not sure where to get this. Pure API research outputs? Scopus?
  # It's not in the Pure API person data.
  orcid = Column(String(20), nullable=True)

  # This scopus ID may be unnecessarily long. Also, some sources claim
  # that a person may (incorrectly, I think) have more than one scopus ID:
  scopus_id = Column(String(35), nullable=True)

  # Apparently there can be multiples of these, from different sources.
  # We use only the one from Scopus for now:
  hindex = Column(Integer, nullable=True)

  emplid = Column(String(11), nullable=True, index=True)
  internet_id = Column(String(15), nullable=True)
  first_name = Column(String(100), nullable=True)
  last_name = Column(String(100), nullable=True)

  # (Y|N): Y if the person is UMN-internal *and* we have added
  # That person's data to the Pure database. Therefore, some
  # UMN employees may be classified as external in Pure.
  pure_internal = Column(String(1), nullable=False) 

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

class PersonScopusId(Base):
  __tablename__ = 'person_scopus_id'
  person_uuid = Column(ForeignKey('person.uuid'), primary_key=True)

  # This scopus ID may be unnecessarily long:
  scopus_id = Column(String(35), primary_key=True)

  def __repr__(self):
    return 'person_uuid: {}, scopus_id: {}'.format(self.person_uuid, self.scopus_id)

# Records all UMN departments in Pure, with a timestamp for the datetime added to this table.
class UmnDept(Base):
  __tablename__ = 'umn_dept'
  deptid = Column(Integer, primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'deptid: {}, timestamp: {}'.format(self.deptid, self.timestamp)

# The hierarchy of Pure UMN-internal organisations.
# Not all Pure organisations are UMN-internal.
# External orgs are not included here.
class PureInternalOrg(Base, BaseNestedSets):
  __tablename__ = 'pure_internal_org'
  id = Column(Integer, primary_key=True)
  pure_uuid = Column(ForeignKey('pure_org.pure_uuid'), nullable=False)

  # De-normalization columns--not really required:
  pure_id = Column(String(50), nullable=True, index=True)
  name_en = Column(String(255))

  pure_org = relationship('PureOrg', backref=backref('pure_internal_org', uselist=False))

  def __repr__(self):
    return 'id: {}, parent_id: {}, lft: {}, rgt: {}, pure_uuid: {}, name_en: {}'.format(self.id, self.parent_id, self.lft, self.rgt, self.pure_uuid, self.name_en)

class PureOrg(Base):
  __tablename__ = 'pure_org'
  pure_uuid = Column(String(36), primary_key=True)
  pure_id = Column(String(50), nullable=True)
  parent_pure_uuid = Column(String(36), nullable=True)
  parent_pure_id = Column(String(50), nullable=True)
  # (Y|N): Y if the org is UMN-internal:
  pure_internal = Column(String(1), nullable=False) 
  type = Column(String(25), nullable=True)
  name_en = Column(String(255), nullable=False)
  name_variant_en = Column(String(255), nullable=True)
  url = Column(String(255), nullable=True)

  # Date the associated record was last modified in Pure.
  pure_modified = Column(DateTime, nullable=True)

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
  person_uuid = Column(ForeignKey('person.uuid'), nullable=False, primary_key=True)
  pure_org_uuid = Column(ForeignKey('pure_org.pure_uuid'), nullable=False, primary_key=True)

  person = relationship('Person', backref="pure_org_associations")
  pure_org = relationship('PureOrg', backref="person_associations")

  def __repr__(self):
    return 'person_uuid: {}, pure_org_uuid: {}'.format(self.pub_uuid, self.person_uuid, self.pure_org_uuid)

# We need this table, in addition to person_pure_org, because we get far more data
# for UMN-internal persons, some of which we use to ensure row uniqueness.
class UmnPersonPureOrg(Base):
  __tablename__ = 'umn_person_pure_org'
  person_uuid = Column(ForeignKey('person.uuid'), nullable=False, primary_key=True)
  pure_org_uuid = Column(ForeignKey('pure_org.pure_uuid'), nullable=False, primary_key=True)

  # De-normalization columns--not really required.
  emplid = Column(String(11), nullable=False)
  pure_person_id = Column(String(11), nullable=False)
  pure_org_id = Column(String(50), nullable=True)

  # We should probably include a job code in the PK instead of this, but we
  # don't have those yet:
  job_description = Column(String(255), nullable=True, primary_key=True)

  employed_as = Column(String(50), nullable=True) # Academic (anything else?)
  staff_type = Column(String(11), nullable=True) # (non)?academic

  # Seems wrong that we should have to add this to the PK, but it's the only
  # way I can get the data to load the first time, at least:
  start_date = Column(DateTime, default=func.current_timestamp(), primary_key=True)

  end_date = Column(DateTime, nullable=True)
  primary = Column(String(1), nullable=True) # (Y|N): Primary affiliation flag.

  person = relationship('Person', backref="umn_pure_org_associations")
  pure_org = relationship('PureOrg', backref="umn_person_associations")

class UmnDeptPureOrg(Base):
  __tablename__ = 'umn_dept_pure_org'
  umn_dept_id = Column(Integer, primary_key=True)
  umn_dept_name = Column(String(255), nullable=True)
  pure_org_uuid = Column(ForeignKey('pure_org.pure_uuid'), nullable=False)

  # De-normalization column--not really required.
  pure_org_id = Column(String(50), nullable=True)

  def __repr__(self):
    return 'umn_dept_id: {}, umn_dept_name: {}, pure_org_uuid: {}, pure_org_id: {}'.format(self.umn_dept_id, self.umn_dept_name, self.pure_org_uuid, self.pure_org_id)

class PureNewStaffDeptDefaults(Base):
  __tablename__ = 'pure_new_staff_dept_defaults'
  deptid = Column(String(10), primary_key=True)
  deptid_descr = Column(String(30), nullable=True)
  pure_org_id = Column(String(50), nullable=True)
  jobcode = Column(String(13), primary_key=True)
  jobcode_descr = Column(String(35), primary_key=True)
  um_college = Column(String(20), nullable=True)
  um_college_descr = Column(String(30), nullable=True)
  default_visibility = Column(String(10), nullable=False)
  default_profiled = Column(String(5), nullable=False)

class PureNewStaffPosDefaults(Base):
  __tablename__ = 'pure_new_staff_pos_defaults'
  jobcode = Column(String(13), primary_key=True)
  jobcode_descr = Column(String(35), nullable=True)
  um_jobcode_group = Column(String(8), nullable=True)
  um_jobcode_group_descr = Column(String(50), nullable=True)
  default_staff_type = Column(String(11), nullable=False)
  default_employed_as = Column(String(50), nullable=False)

## Views

class AffiliateJobs(Base):
  __table__ = Table(
    'affiliate_jobs',
    Base.metadata,
    Column('emplid', String(11), primary_key=True),
    Column('jobcode', String(5), primary_key=True),
    Column('deptid', Integer, primary_key=True),
    autoload=True,
    autoload_with=engine
 )

class AllJobs(Base):
  __table__ = Table(
    'all_jobs',
    Base.metadata,
    Column('emplid', String(11), primary_key=True),
    Column('jobcode', String(5), primary_key=True),
    Column('deptid', Integer, primary_key=True),
    autoload=True,
    autoload_with=engine
 )

class EmployeeJobs(Base):
  __table__ = Table(
    'employee_jobs',
    Base.metadata,
    Column('emplid', String(11), primary_key=True),
    Column('jobcode', String(5), primary_key=True),
    Column('deptid', Integer, primary_key=True),
    autoload=True,
    autoload_with=engine
 )

class Demographics(Base):
  __table__ = Table(
    'demographics',
    Base.metadata,
    Column('emplid', String(11), primary_key=True),
    autoload=True,
    autoload_with=engine
 )

class PureEligibleDemog(Base):
  __table__ = Table(
    'pure_eligible_demog',
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

class PureEligibleEmpJob(Base):
  __table__ = Table(
    'pure_eligible_emp_job',
    Base.metadata,
    Column('emplid', String(11), primary_key=True),
    Column('position_nbr', String(8), primary_key=True),
    Column('effdt', DateTime, primary_key=True),
    Column('effseq', Integer, primary_key=True),
    autoload=True,
    autoload_with=engine
 )

class PureEligibleAffJob(Base):
  __table__ = Table(
    'pure_eligible_aff_job',
    Base.metadata,
    Column('emplid', String(11), primary_key=True),
    Column('um_affiliate_id', String(2), primary_key=True),
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

class AllJobsNew(Base):
  __tablename__ = 'all_jobs_new'
  emplid = Column(String(11), primary_key=True)
  empl_rcdno = Column(String(40), nullable=True)
  name = Column(String(50), nullable=True)
  jobcode = Column(String(13), primary_key=True)
  jobcode_descr = Column(String(35), nullable=True)
  job_indicator = Column(String(40), primary_key=True)
  empl_status = Column(String(4), nullable=True)
  paygroup = Column(String(12), nullable=True)
  deptid = Column(String(10), primary_key=True)
  deptid_descr = Column(String(30), nullable=True)
  um_jobcode_group = Column(String(8), nullable=True)
  um_college = Column(String(20), nullable=True)
  um_college_descr = Column(String(30), nullable=True)
  campus = Column(String(20), nullable=True)
  um_zdeptid = Column(String(80), nullable=True)
  um_zdeptid_descr = Column(String(30), nullable=True)
  status_flg = Column(String(1), nullable=True)
  record_source = Column(String(1), nullable=True)
  job_entry_dt = Column(DateTime, nullable=True)
  position_entry_dt = Column(DateTime, nullable=True)
  calculated_start_dt = Column(DateTime, nullable=True)

class AllJobsPrevious(Base):
  __tablename__ = 'all_jobs_previous'
  emplid = Column(String(11), primary_key=True)
  empl_rcdno = Column(String(40), nullable=True)
  name = Column(String(50), nullable=True)
  jobcode = Column(String(13), primary_key=True)
  jobcode_descr = Column(String(35), nullable=True)
  job_indicator = Column(String(40), primary_key=True)
  empl_status = Column(String(4), nullable=True)
  paygroup = Column(String(12), nullable=True)
  deptid = Column(String(10), primary_key=True)
  deptid_descr = Column(String(30), nullable=True)
  um_jobcode_group = Column(String(8), nullable=True)
  um_college = Column(String(20), nullable=True)
  um_college_descr = Column(String(30), nullable=True)
  campus = Column(String(20), nullable=True)
  um_zdeptid = Column(String(80), nullable=True)
  um_zdeptid_descr = Column(String(30), nullable=True)
  status_flg = Column(String(1), nullable=True)
  record_source = Column(String(1), nullable=True)
  job_entry_dt = Column(DateTime, nullable=True)
  position_entry_dt = Column(DateTime, nullable=True)
  calculated_start_dt = Column(DateTime, nullable=True)

class PureEligibleAffJobNew(Base):
  __tablename__ = 'pure_eligible_aff_job_new'
  emplid = Column(String(11), primary_key=True)
  name = Column(String(50), nullable=True)
  um_affiliate_id = Column(String(2), primary_key=True)
  effdt = Column(DateTime, primary_key=True)
  um_affil_relation = Column(String(6), nullable=True)
  title = Column(String(35), nullable=True)
  deptid = Column(String(10), primary_key=True)
  deptid_descr = Column(String(30), nullable=True)
  status = Column(String(1), nullable=True)
  um_college = Column(String(20), nullable=True)
  um_college_descr = Column(String(30), nullable=True)
  um_campus = Column(String(20), nullable=True)
  um_zdeptid = Column(String(80), nullable=True)
  um_zdeptid_descr = Column(String(30), nullable=True)
  status_flg = Column(String(1), nullable=True)

# A history of changes to Pure-eligible affiliate jobs.
class PureEligibleAffJobChngHst(Base):
  __tablename__ = 'pure_eligible_aff_job_chng_hst'
  emplid = Column(String(11), primary_key=True)
  name = Column(String(50), nullable=True)
  um_affiliate_id = Column(String(2), nullable=True)
  effdt = Column(DateTime, nullable=True)
  um_affil_relation = Column(String(6), nullable=True)
  title = Column(String(35), nullable=True)
  deptid = Column(String(10), nullable=True)
  deptid_descr = Column(String(30), nullable=True)
  status = Column(String(1), nullable=True)
  um_college = Column(String(20), nullable=True)
  um_college_descr = Column(String(30), nullable=True)
  um_campus = Column(String(20), nullable=True)
  um_zdeptid = Column(String(80), nullable=True)
  um_zdeptid_descr = Column(String(30), nullable=True)
  status_flg = Column(String(1), nullable=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), primary_key=True)

class PureEligibleEmpJobNew(Base):
  __tablename__ = 'pure_eligible_emp_job_new'
  emplid = Column(String(11), primary_key=True)
  empl_rcdno = Column(String(40), primary_key=True)
  effdt = Column(DateTime, primary_key=True)
  effseq = Column(Integer, primary_key=True)
  name = Column(String(50), nullable=True)
  position_nbr = Column(String(8), primary_key=True)
  jobcode = Column(String(13), primary_key=True)
  jobcode_descr = Column(String(35), nullable=True)
  job_indicator = Column(String(40), nullable=True)
  empl_status = Column(String(4), primary_key=True)
  paygroup = Column(String(12), nullable=True)
  deptid = Column(String(10), primary_key=True)
  deptid_descr = Column(String(30), nullable=True)
  um_jobcode_group = Column(String(8), nullable=True)
  um_college = Column(String(20), nullable=True)
  um_college_descr = Column(String(30), nullable=True)
  rrc = Column(String(20), nullable=True)
  um_zdeptid = Column(String(80), nullable=True)
  um_zdeptid_descr = Column(String(30), nullable=True)
  status_flg = Column(String(1), primary_key=True)
  job_terminated = Column(String(1), nullable=True)
  last_date_worked = Column(DateTime, nullable=True)
  job_entry_dt = Column(DateTime, nullable=True)
  position_entry_dt = Column(DateTime, nullable=True)

# A history of changes to Pure-eligible employee jobs.
class PureEligibleEmpJobChngHst(Base):
  __tablename__ = 'pure_eligible_emp_job_chng_hst'
  emplid = Column(String(11), primary_key=True)
  empl_rcdno = Column(String(40), nullable=True)
  effdt = Column(DateTime, nullable=True)
  effseq = Column(Integer, nullable=True)
  name = Column(String(50), nullable=True)
  position_nbr = Column(String(8), nullable=True)
  jobcode = Column(String(13), nullable=True)
  jobcode_descr = Column(String(35), nullable=True)
  job_indicator = Column(String(40), nullable=True)
  empl_status = Column(String(4), nullable=True)
  paygroup = Column(String(12), nullable=True)
  deptid = Column(String(10), nullable=True)
  deptid_descr = Column(String(30), nullable=True)
  um_jobcode_group = Column(String(8), nullable=True)
  um_college = Column(String(20), nullable=True)
  um_college_descr = Column(String(30), nullable=True)
  rrc = Column(String(20), nullable=True)
  um_zdeptid = Column(String(80), nullable=True)
  um_zdeptid_descr = Column(String(30), nullable=True)
  status_flg = Column(String(1), nullable=True)
  job_terminated = Column(String(1), nullable=True)
  last_date_worked = Column(DateTime, nullable=True)
  job_entry_dt = Column(DateTime, nullable=True)
  position_entry_dt = Column(DateTime, nullable=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), primary_key=True)

## Tables that store records retrieved via the Pure web services API.

class PureApiPub(Base):
  __tablename__ = 'pure_api_pub'
  uuid = Column(String(36), primary_key=True)
  json = Column(Text, nullable=False)
  created = Column(DateTime, nullable=False)
  modified = Column(DateTime, nullable=False, primary_key=True)
  downloaded = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'uuid: {}, created: {}, modified: {}, downloaded: {}'.format(self.uuid, self.created, self.modified, self.downloaded)

