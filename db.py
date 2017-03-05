import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(find_dotenv())

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
  Session = sessionmaker()
  Session.configure(bind=engine(db_name))
  return Session()
