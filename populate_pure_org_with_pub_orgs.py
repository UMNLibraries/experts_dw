# One-off to import the orgs (all external, it seems) associated with publication records.
import env
from pureapi import client, parser
from models import Pub, PureOrg

import db
session = db.session('hotel')

import uuid
import pprint
pp = pprint.PrettyPrinter(indent=2)

def db_org_exists(record_org_pure_uuid):
  db_org = (
    session.query(PureOrg)
    .filter(PureOrg.pure_uuid == record_org_pure_uuid)
    .one_or_none()
  )
  if db_org is None:
    return False
  else:
    return True

def db_org(record_org):
  return PureOrg(
    pure_uuid = record_org['pure_uuid'],
    parent_pure_uuid = record_org['parent_pure_uuid'],
    pure_id = record_org['pure_id'],
    parent_pure_id = record_org['parent_pure_id'],
    name_en = record_org['name_en'],
    name_variant_en = record_org['name_variant_en'],
    type = record_org['type'],
    pure_internal = record_org['pure_internal'],
    url = record_org['url']
  )

# Keep track of all orgs we've seen so far:
orgs_seen = {}

params = { 
  'window.size': 20,
  'namespaces': 'remove',
  'rendering': 'xml_long',
}

for response in client.get_all('publication', params):
  for record in parser.records(response.text):
    type = record.attrib['type']
    if type != 'stab:ContributionToJournalType':
      continue

    pure_pub = parser.publication(record)

    for record_org in pure_pub['associated_external_organisations']:
      # These are all external orgs, so...
      if (record_org['pure_uuid'] not in orgs_seen) and (not db_org_exists(record_org['pure_uuid'])):
        session.add(db_org(record_org))
      orgs_seen[record_org['pure_uuid']] = record_org

    for record_org_assoc in pure_pub['organisation_associations']:
      record_org = record_org_assoc['organisation']
      if (record_org['pure_uuid'] not in orgs_seen) and (not db_org_exists(record_org['pure_uuid'])):
        session.add(db_org(record_org))
      orgs_seen[record_org['pure_uuid']] = record_org

    owner_org = pure_pub['owner_organisation']
    if (owner_org['pure_uuid'] not in orgs_seen) and (not db_org_exists(owner_org['pure_uuid'])):
      session.add(db_org(owner_org))
    orgs_seen[owner_org['pure_uuid']] = owner_org

    for person_association in pure_pub['person_associations']:
      if 'organisation_associations' in person_association:
        for org_assoc in person_association['organisation_associations']:
          record_org = org_assoc['organisation']
          if (record_org['pure_uuid'] not in orgs_seen) and (not db_org_exists(record_org['pure_uuid'])):
            session.add(db_org(record_org))
          orgs_seen[record_org['pure_uuid']] = record_org
      # For some strange reason, some person_associaions do not contain person records:
      if 'person' in person_association:
        for org_assoc in person_association['person']['organisation_associations']:
          record_org = org_assoc['organisation']
          if (record_org['pure_uuid'] not in orgs_seen) and (not db_org_exists(record_org['pure_uuid'])):
            session.add(db_org(record_org))
          orgs_seen[record_org['pure_uuid']] = record_org
        for staff_org_assoc in person_association['person']['staff_organisation_associations']:
          record_org = staff_org_assoc['organisation']
          if (record_org['pure_uuid'] not in orgs_seen) and (not db_org_exists(record_org['pure_uuid'])):
            session.add(db_org(record_org))
          orgs_seen[record_org['pure_uuid']] = record_org
      
  session.commit()
