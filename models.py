from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_mptt.mixins import BaseNestedSets

# Would like to name constraints, but Oracle limits names to 30 characters!
#import common
#Base = declarative_base(metadata=common.metadata)
Base = declarative_base()

class Person(Base):
  __tablename__ = 'person'
  uuid = Column(String(36), primary_key=True)
  pure_uuid = Column(String(36), nullable=True)

  # May be emplid or old scival_id. Seems emplids may contain more
  # characters than scival ids, so using the emplid length:
  pure_id = Column(String(11), nullable=True)

  orcid = Column(String(20), nullable=True)

  # This scopus ID may be unnecessarily long. Also, some sources claim
  # that a person may (incorrectly, I think) have more than one scopus ID:
  scopus_id = Column(String(35), nullable=True)

  # Apparently there can be multiples of these, from different sources.
  # We use only the one from Scopus for now:
  hindex = Column(Integer, nullable=True)

  emplid = Column(String(11), nullable=True)
  internet_id = Column(String(15), nullable=True)
  first_name = Column(String(100), nullable=True)
  last_name = Column(String(100), nullable=True)

  def __repr__(self):
    return 'uuid: {}'.format(self.uuid)

class PureOrg(Base, BaseNestedSets):
  __tablename__ = 'pure_org'
  id = Column(Integer, primary_key=True)
  pure_id = Column(String(50), unique=True, nullable=False)
  type = Column(String(25))
  name_en = Column(String(255))

  def __repr__(self):
    return 'id: {}, pure_id: {}, type: {}, name_en: {}'.format(self.id, self.pure_id, self.type, self.name_en)

class UmnDeptPureOrgMap(Base):
  __tablename__ = 'umn_dept_pure_org_map'
  umn_dept_id = Column(Integer, primary_key=True)
  umn_dept_name = Column(String(255), nullable=True)
  pure_org_id = Column(ForeignKey('pure_org.pure_id'), nullable=False)
  pure_org = relationship('PureOrg', cascade="all, delete-orphan", single_parent=True)

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
