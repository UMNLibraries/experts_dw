# One-off to populate the Pure Organisations Tree table, assumed to be empty.

import db
session = db.session('hotel')
from models import PureOrg

import csv
import sys
filename = sys.argv[1]

with open(filename) as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    pure_id = row[0]
    type = row[1]
    name_en = row[2]

    org = (
      session.query(PureOrg)
      .filter(PureOrg.pure_id == pure_id)
      .one()
    )
    org.type = type
    org.name_en = name_en

session.commit()
