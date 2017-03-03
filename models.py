from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class MdsPerson(Base):
  __tablename__ = 'mds_person'
  emplid = Column(String(11), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)

  def __repr__(self):
    return 'emplid: {}, timestamp: {}'.format(self.emplid, self.timestamp)

# The Scival ID was automatically-generated for Elsevier's predecessor-to-Pure
# product, SciVal. After moving to Pure we started using UMN's EmplID for new
# persons, but kept the SciVal ID for existing persons. This list should be
# static, neither growing nor shrinking nor changing.

class MdsPersonScivalId(Base):
  __tablename__ = 'mds_person_scival_id'
  scival_id = Column(Integer, primary_key=True)
  emplid = Column(ForeignKey('mds_person.emplid'), nullable=False)
  timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)
  mds_person = relationship('MdsPerson')

  def __repr__(self):
    return 'scival_id: {}, emplid: {}, timestamp: {}'.format(self.scival_id, self.emplid, self.timestamp)

# The following group of tables all track data from ps_dwhr_demo_addr, which does
# not have an effective date (effdt) column.

class MdsPersonInternetId(Base):
  __tablename__ = 'mds_person_internet_id'
  internet_id = Column(String(15), nullable=False)
  emplid = Column(ForeignKey('mds_person.emplid'), nullable=False)
  timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)
  mds_person = relationship('MdsPerson')

  def __repr__(self):
    return 'internet_id: {}, emplid: {}, timestamp: {}'.format(self.internet_id, self.emplid, self.timestamp)

class MdsPersonFirstName(Base):
  __tablename__ = 'mds_person_first_name'
  first_name = Column(String(30), nullable=False)
  emplid = Column(ForeignKey('mds_person.emplid'), nullable=False)
  timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)
  mds_person = relationship('MdsPerson')

  def __repr__(self):
    return 'first_name: {}, emplid: {}, timestamp: {}'.format(self.first_name, self.emplid, self.timestamp)

class MdsPersonMiddleName(Base):
  __tablename__ = 'mds_person_middle_name'
  middle_name = Column(String(30), nullable=False)
  emplid = Column(ForeignKey('mds_person.emplid'), nullable=False)
  timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)
  mds_person = relationship('MdsPerson')

  def __repr__(self):
    return 'middle_name: {}, emplid: {}, timestamp: {}'.format(self.middle_name, self.emplid, self.timestamp)

class MdsPersonLastName(Base):
  __tablename__ = 'mds_person_last_name'
  last_name = Column(String(30), nullable=False)
  emplid = Column(ForeignKey('mds_person.emplid'), nullable=False)
  timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)
  mds_person = relationship('MdsPerson')

  def __repr__(self):
    return 'last_name: {}, emplid: {}, timestamp: {}'.format(self.last_name, self.emplid, self.timestamp)

class MdsPersonNameSuffix(Base):
  __tablename__ = 'mds_person_name_suffix'
  name_suffix = Column(String(15), nullable=False)
  emplid = Column(ForeignKey('mds_person.emplid'), nullable=False)
  timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)
  mds_person = relationship('MdsPerson')

  def __repr__(self):
    return 'name_suffix: {}, emplid: {}, timestamp: {}'.format(self.name_suffix, self.emplid, self.timestamp)

class MdsPersonInstEmailAddr(Base):
  __tablename__ = 'mds_person_inst_email_addr'
  inst_email_addr = Column(String(15), nullable=False)
  emplid = Column(ForeignKey('mds_person.emplid'), nullable=False)
  timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)
  mds_person = relationship('MdsPerson')

  def __repr__(self):
    return 'inst_email_addr: {}, emplid: {}, timestamp: {}'.format(self.inst_email_addr, self.emplid, self.timestamp)

class MdsPersonTenureFlag(Base):
  __tablename__ = 'mds_person_tenure_flag'
  tenure_flag = Column(String(1), nullable=False)
  emplid = Column(ForeignKey('mds_person.emplid'), nullable=False)
  timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)
  mds_person = relationship('MdsPerson')

  def __repr__(self):
    return 'tenure_flag: {}, emplid: {}, timestamp: {}'.format(self.tenure_flag, self.emplid, self.timestamp)

class MdsPersonTenureTrackFlag(Base):
  __tablename__ = 'mds_person_tenure_track_flag'
  tenure_track_flag = Column(String(1), nullable=False)
  emplid = Column(ForeignKey('mds_person.emplid'), nullable=False)
  timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)
  mds_person = relationship('MdsPerson')

  def __repr__(self):
    return 'tenure_track_flag: {}, emplid: {}, timestamp: {}'.format(self.tenure_track_flag, self.emplid, self.timestamp)

class MdsPersonPrimaryEmplRcdno(Base):
  __tablename__ = 'mds_person_primary_empl_rcdno'
  primary_empl_rcdno = Column(Integer(38), nullable=False)
  emplid = Column(ForeignKey('mds_person.emplid'), nullable=False)
  timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)
  mds_person = relationship('MdsPerson')

  def __repr__(self):
    return 'primary_empl_rcdno: {}, emplid: {}, timestamp: {}'.format(self.primary_empl_rcdno, self.emplid, self.timestamp)
