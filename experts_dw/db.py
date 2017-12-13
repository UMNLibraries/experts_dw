import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_mptt import mptt_sessionmaker

def engine(db_name):
  # db_name must be the generic part of the service name,
  # without the (tst|prd).oit suffix, e.g. 'dwe' or 'hotel'.
  return create_engine(
    "oracle://%s:\"%s\"@%s" % (
      os.environ.get('DB_USER'),
      os.environ.get('DB_PASS'),
      os.environ.get(db_name.upper() + '_DB_SERVICE_NAME'),
    )
  )

def session(db_name):
  # Original:
  #Session = sessionmaker()
  # mptt docs:
  #Session = mptt_sessionmaker(sessionmaker(bind=engine))
  # This didn't work:
  #Session = mptt_sessionmaker(sessionmaker())

  #Session.configure(bind=engine(db_name))
  Session = mptt_sessionmaker(sessionmaker(bind=engine(db_name)))
  return Session()
