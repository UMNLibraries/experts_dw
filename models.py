from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_mptt.mixins import BaseNestedSets

# Would like to name constraints, but Oracle limits names to 30 characters!
#import common
#Base = declarative_base(metadata=common.metadata)
Base = declarative_base()

class ResearchOutput(Base):
  __tablename__ = 'research_output'
  uuid = Column(String(36), primary_key=True)
  pure_uuid = Column(String(36), nullable=True)

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
  issue = Column(String(25), nullable=True)
  pages = Column(String(50), nullable=True)

  # Total number of citations of the output. We call it a "totatl" because Pure
  # also provides citation counts per year, which we may decide to use later.
  citation_total = Column(Integer, nullable=True)

class ResearchOutputPersonMap(Base):
  __tablename__ = 'research_output_person_map'
  research_output_uuid = Column(ForeignKey('research_output.uuid'), nullable=False, primary_key=True)
  person_uuid = Column(ForeignKey('person.uuid'), nullable=False, primary_key=True)
  emplid = Column(String(11), nullable=True, index=True)

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
  person_pure_internal = Column(String(1), nullable=True) 

  research_output = relationship('ResearchOutput', cascade="all, delete-orphan", single_parent=True)
  person = relationship('Person', cascade="all, delete-orphan", single_parent=True)

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

  def __repr__(self):
    return 'uuid: {}'.format(self.uuid)

# The hierarchy of Pure UMN-internal organisations.
# Not all Pure organisations are UMN-internal.
# External orgs are not included here.
class PureInternalOrg(Base, BaseNestedSets):
  __tablename__ = 'pure_internal_org'
  id = Column(Integer, primary_key=True)
  pure_uuid = Column(String(36), nullable=True)

  # De-normalization columns--not really required:
  pure_id = Column(String(50), nullable=True, index=True)
  type = Column(String(25))
  name_en = Column(String(255))

  def __repr__(self):
  #  return 'id: {}, pure_uuid: {}, pure_id: {}, type: {}, name_en: {}'.format(self.id, self.pure_uuid, self.pure_id, self.type, self.name_en)
    return 'id: {}, pure_id: {}, type: {}, name_en: {}'.format(self.id, self.pure_id, self.type, self.name_en)

class PureOrg(Base):
  __tablename__ = 'pure_org'
  pure_uuid = Column(String(36), primary_key=True)
  pure_id = Column(String(50), nullable=True)
  type = Column(String(25))
  name_en = Column(String(255))

  def __repr__(self):
    return 'pure_uuid: {}, pure_id: {}, type: {}, name_en: {}'.format(self.pure_uuid, self.pure_id, self.type, self.name_en)

# TODO: Do we need this table? Maybe a generic PersonOrg table can replace it.
class UmnPersonPureOrgMap(Base):
  __tablename__ = 'umn_person_pure_org_map'
  person_uuid = Column(ForeignKey('person.uuid'), nullable=False, primary_key=True)
  emplid = Column(String(11), nullable=False)
  pure_person_id = Column(String(11), nullable=False)
  #pure_org_id = Column(ForeignKey('pure_org.pure_id'), primary_key=True)
  pure_org_id = Column(String(50), primary_key=True)

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
  #pure_org = relationship('PureOrg', cascade="all, delete-orphan", single_parent=True)
  person = relationship('Person', cascade="all, delete-orphan", single_parent=True)

class UmnDeptPureOrgMap(Base):
  __tablename__ = 'umn_dept_pure_org_map'
  umn_dept_id = Column(Integer, primary_key=True)
  umn_dept_name = Column(String(255), nullable=True)
  #pure_org_id = Column(ForeignKey('pure_org.pure_id'), nullable=False)
  pure_org_id = Column(String(50), nullable=True)
  #pure_org = relationship('PureOrg', cascade="all, delete-orphan", single_parent=True)

  def __repr__(self):
    return 'umn_dept_id: {}, umn_dept_name: {}, pure_org_id: {}'.format(self.umn_dept_id, self.umn_dept_name, self.pure_org_id)

## Master Dataset tables. Names all start with 'mds_'.

class MdsPerson(Base):
  __tablename__ = 'mds_person'
  uuid = Column(String(36), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'uuid: {}, timestamp: {}'.format(self.uuid, self.timestamp)

class MdsPersonEmplid(Base):
  __tablename__ = 'mds_person_emplid'
  emplid = Column(String(11), nullable=True)
  uuid = Column(ForeignKey('mds_person.uuid'), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), primary_key=True)
  mds_person = relationship('MdsPerson', cascade="all, delete-orphan", single_parent=True)

  def __repr__(self):
    return 'emplid: {}, uuid: {}, timestamp: {}'.format(self.emplid, self.uuid, self.timestamp)

# The Scival ID was automatically-generated for Elsevier's predecessor-to-Pure
# product, SciVal. After moving to Pure we started using UMN's EmplID for new
# persons, but kept the SciVal ID for existing persons. This list should be
# static, neither growing nor shrinking nor changing.

class MdsPersonScivalId(Base):
  __tablename__ = 'mds_person_scival_id'
  scival_id = Column(Integer, nullable=True)
  uuid = Column(ForeignKey('mds_person.uuid'), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), primary_key=True)
  mds_person = relationship('MdsPerson', cascade="all, delete-orphan", single_parent=True)

  def __repr__(self):
    return 'scival_id: {}, uuid: {}, timestamp: {}'.format(self.scival_id, self.uuid, self.timestamp)

# The following group of tables all track data from ps_dwhr_demo_addr, which does
# not have an effective date (effdt) column.

class MdsPersonInternetId(Base):
  __tablename__ = 'mds_person_internet_id'
  internet_id = Column(String(15), nullable=True)
  uuid = Column(ForeignKey('mds_person.uuid'), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), primary_key=True)
  mds_person = relationship('MdsPerson', cascade="all, delete-orphan", single_parent=True)

  def __repr__(self):
    return 'internet_id: {}, uuid: {}, timestamp: {}'.format(self.internet_id, self.uuid, self.timestamp)

class MdsPersonPreferredName(Base):
  __tablename__ = 'mds_person_preferred_name'
  preferred_name = Column(String(255), nullable=True)
  uuid = Column(ForeignKey('mds_person.uuid'), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), primary_key=True)
  mds_person = relationship('MdsPerson', cascade="all, delete-orphan", single_parent=True)

  def __repr__(self):
    return 'preferred_name: {}, uuid: {}, timestamp: {}'.format(self.preferred_name, self.uuid, self.timestamp)

class MdsPersonFirstName(Base):
  __tablename__ = 'mds_person_first_name'
  first_name = Column(String(100), nullable=True)
  uuid = Column(ForeignKey('mds_person.uuid'), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), primary_key=True)
  mds_person = relationship('MdsPerson', cascade="all, delete-orphan", single_parent=True)

  def __repr__(self):
    return 'first_name: {}, uuid: {}, timestamp: {}'.format(self.first_name, self.uuid, self.timestamp)

class MdsPersonMiddleName(Base):
  __tablename__ = 'mds_person_middle_name'
  middle_name = Column(String(100), nullable=True)
  uuid = Column(ForeignKey('mds_person.uuid'), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), primary_key=True)
  mds_person = relationship('MdsPerson', cascade="all, delete-orphan", single_parent=True)

  def __repr__(self):
    return 'middle_name: {}, uuid: {}, timestamp: {}'.format(self.middle_name, self.uuid, self.timestamp)

class MdsPersonLastName(Base):
  __tablename__ = 'mds_person_last_name'
  last_name = Column(String(100), nullable=True)
  uuid = Column(ForeignKey('mds_person.uuid'), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), primary_key=True)
  mds_person = relationship('MdsPerson', cascade="all, delete-orphan", single_parent=True)

  def __repr__(self):
    return 'last_name: {}, uuid: {}, timestamp: {}'.format(self.last_name, self.uuid, self.timestamp)

class MdsPersonNameSuffix(Base):
  __tablename__ = 'mds_person_name_suffix'
  name_suffix = Column(String(30), nullable=True)
  uuid = Column(ForeignKey('mds_person.uuid'), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), primary_key=True)
  mds_person = relationship('MdsPerson', cascade="all, delete-orphan", single_parent=True)

  def __repr__(self):
    return 'name_suffix: {}, uuid: {}, timestamp: {}'.format(self.name_suffix, self.uuid, self.timestamp)

class MdsPersonInstlEmailAddr(Base):
  __tablename__ = 'mds_person_instl_email_addr'
  instl_email_addr = Column(String(70), nullable=True)
  uuid = Column(ForeignKey('mds_person.uuid'), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), primary_key=True)
  mds_person = relationship('MdsPerson', cascade="all, delete-orphan", single_parent=True)

  def __repr__(self):
    return 'instl_email_addr: {}, uuid: {}, timestamp: {}'.format(self.inst_email_addr, self.uuid, self.timestamp)

class MdsPersonTenureFlag(Base):
  __tablename__ = 'mds_person_tenure_flag'
  tenure_flag = Column(String(1), nullable=True)
  uuid = Column(ForeignKey('mds_person.uuid'), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), primary_key=True)
  mds_person = relationship('MdsPerson', cascade="all, delete-orphan", single_parent=True)

  def __repr__(self):
    return 'tenure_flag: {}, uuid: {}, timestamp: {}'.format(self.tenure_flag, self.uuid, self.timestamp)

class MdsPersonTenureTrackFlag(Base):
  __tablename__ = 'mds_person_tenure_track_flag'
  tenure_track_flag = Column(String(1), nullable=True)
  uuid = Column(ForeignKey('mds_person.uuid'), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), primary_key=True)
  mds_person = relationship('MdsPerson', cascade="all, delete-orphan", single_parent=True)

  def __repr__(self):
    return 'tenure_track_flag: {}, uuid: {}, timestamp: {}'.format(self.tenure_track_flag, self.uuid, self.timestamp)

class MdsPersonPrimaryEmplRcdno(Base):
  __tablename__ = 'mds_person_primary_empl_rcdno'
  primary_empl_rcdno = Column(Integer, nullable=True)
  uuid = Column(ForeignKey('mds_person.uuid'), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), primary_key=True)
  mds_person = relationship('MdsPerson', cascade="all, delete-orphan", single_parent=True)

  def __repr__(self):
    return 'primary_empl_rcdno: {}, uuid: {}, timestamp: {}'.format(self.primary_empl_rcdno, self.uuid, self.timestamp)
