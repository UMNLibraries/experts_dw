import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
connection_string = "oracle://%s:\"%s\"@%s" % (
  os.environ.get("DB_USER"),
  os.environ.get("DB_PASS"),
  os.environ.get("DB_SERVICE_NAME"),
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

engine = create_engine(connection_string)
Session = sessionmaker()
Session.configure(bind=engine)

session = Session()

def get_session():
  return session
