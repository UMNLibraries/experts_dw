# One-off to populate the person master dataset table, assumed to be empty.

import db
session = db.session('hotel')

from models import MdsPerson, MdsPersonEmplid

import csv
import sys
import uuid
filename = sys.argv[1]
with open(filename) as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    emplid = row[1]
    person_uuid = uuid.uuid4()
    person = MdsPerson(uuid=person_uuid)
    person_emplid = 
      session.query(MdsPersonEmplid)
      .filter(MdsPersonEmplid.emplid == emplid)
      .one_or_none()
    )
    person_emplid.uuid = person_uuid
    session.add(person)

session.commit()
