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
from models import Base, Person

engine = create_engine(connection_string)
Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

session = Session()

import csv
import sys
filename = sys.argv[1]
with open(filename) as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    person = Person(emplid=row[1])
    session.add(person)

session.commit()
