# One-off to populate the person master dataset table, assumed to be empty.

import db
session = db.session('hotel')

from models import MdsPerson

import csv
import sys
filename = sys.argv[1]
with open(filename) as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    person = MdsPerson(emplid=row[1])
    session.add(person)

session.commit()
