# One-off to populate the umn_person_pure_org_map table, assumed to be empty.

import db
session = db.session('hotel')
from models import UmnPersonPureOrgMap, Person, PureOrg
import datetime

import csv
import sys
filename = sys.argv[1]

with open(filename) as csvfile:
  reader = csv.reader(csvfile)
  for row in reader:
    pure_person_id = row[1]
    pure_org_id = row[2]
    job_description = row[3]
    employed_as = row[4]
    staff_type = row[5]
    start_date = row[7]
    end_date = row[8]
    primary = 'Y' if row[13] == 'Yes' else None

    person = (
      session.query(Person)
      .filter(Person.pure_id == pure_person_id)
      .one_or_none()
    )
    if person == None:
      print('No person found with pure_id: {}'.format(pure_person_id))
      continue
    if person.emplid == None:
      print('No emplid found for person with pure_id: {}'.format(pure_person_id))
      continue

    pure_org = (
      session.query(PureOrg)
      .filter(PureOrg.pure_id == pure_org_id)
      .one_or_none()
    )
    if pure_org == None:
      print('No pure_org found with pure_id: {}'.format(pure_org_id))
      continue

    person_org_map = UmnPersonPureOrgMap(
      person_uuid = person.uuid,
      emplid = person.emplid,
      pure_person_id = pure_person_id,
      pure_org_id = pure_org_id,
      job_description = job_description,
      employed_as = employed_as,
      staff_type = staff_type,
      primary = primary
    )
    if not (start_date == None or start_date == ''):
      person_org_map.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    if not (end_date == None or end_date == ''):
      person_org_map.end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    session.add(person_org_map)

session.commit()
