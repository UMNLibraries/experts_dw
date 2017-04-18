# One-off to populate the umn_dept_pure_org_map table, assumed to be empty.

import db
session = db.session('hotel')
from models import UmnDeptPureOrgMap, PureOrg

import csv
import sys
filename = sys.argv[1]

with open(filename) as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    umn_dept_id = int(row[0])
    pure_org_id = row[1]
    umn_dept_name = row[2]

    pure_org = (
      session.query(PureOrg)
      .filter(PureOrg.pure_id == pure_org_id)
      .one_or_none()
    )

    # Some Pure Org IDs appear to be missing from the PureOrg table:
    if (pure_org == None):
      print (
        'umn_dept_id: {}, pure_org_id: {}, umn_dept_name: {}'.format(
          umn_dept_id,
          pure_org_id,
          umn_dept_name
        )
      )
      continue

    dept_org_map = UmnDeptPureOrgMap(
      umn_dept_id = int(row[0]),
      pure_org_id = pure_org_id,
      umn_dept_name = row[2]
    )
    session.add(dept_org_map)

session.commit()
