# One-off to populate the person master dataset table, assumed to be empty.

import db
session = db.session('hotel')

from models import MdsPersonScivalId

import csv
import sys
filename = sys.argv[1]
with open(filename) as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    # The first element is a SciVal ID only if it differs from the second element, which is always an emplid:
    if row[0] == row[1]:
      continue
    person_scival_id = MdsPersonScivalId(scival_id=int(row[0]), emplid=row[1])
    session.add(person_scival_id)

session.commit()
