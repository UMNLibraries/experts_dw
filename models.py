from sqlalchemy import Column, DateTime, String, Integer, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Person(Base):
  __tablename__ = 'person'
  emplid = Column(String(11), primary_key=True)
  timestamp = Column(DateTime, default=func.current_timestamp())

  def __repr__(self):
    return 'emplid: {}, timestamp: {}'.format(self.emplid, self.timestamp)
