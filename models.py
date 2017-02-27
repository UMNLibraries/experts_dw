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

class MdsPersonScivalId(Base):
  __tablename__ = 'mds_person_scival_id'
  scival_id = Column(Integer, primary_key=True)
  emplid = Column(ForeignKey('mds_person.emplid'), nullable=False)
  timestamp = Column(DateTime, default=func.current_timestamp(), nullable=False)
  mds_person = relationship('MdsPerson')

  def __repr__(self):
    return 'scival_id: {}, emplid: {}, timestamp: {}'.format(self.scival_id, self.emplid, self.timestamp)
