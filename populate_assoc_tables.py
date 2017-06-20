import env
from pureapi import client, parser
from models import Pub, Person, PureOrg, PersonPureOrg, PubPerson, PubPersonPureOrg

import db
session = db.session('hotel')

from datetime import date
import uuid
import pprint
pp = pprint.PrettyPrinter(indent=2)

def find_db_person_pure_org(person_uuid, record_org_pure_uuid):
  return (
    session.query(PersonPureOrg)
    .filter(
      PersonPureOrg.person_uuid == person_uuid,
      PersonPureOrg.pure_org_uuid == record_org_pure_uuid,
    )
    .one_or_none()
  )

def find_db_pub_person_pure_org(pub_uuid, person_uuid, record_org_pure_uuid):
  return (
    session.query(PubPersonPureOrg)
    .filter(
      PubPersonPureOrg.pub_uuid == pub_uuid,
      PubPersonPureOrg.person_uuid == person_uuid,
      PubPersonPureOrg.pure_org_uuid == record_org_pure_uuid
    )
    .one_or_none()
  )

def find_db_pub_person(person_uuid, pub_uuid):
  return (
    session.query(PubPerson)
    .filter(
      PubPerson.person_uuid == person_uuid,
      PubPerson.pub_uuid == pub_uuid,
    )
    .one_or_none()
  )

def find_db_pub(record_pub_pure_uuid):
  return (
    session.query(Pub)
    .filter(Pub.pure_uuid == record_pub_pure_uuid)
    .one_or_none()
  )

def find_db_person(record_person_pure_uuid):
  return (
    session.query(Person)
    .filter(Person.pure_uuid == record_person_pure_uuid)
    .one_or_none()
  )

def find_db_org(record_org_pure_uuid):
  return (
    session.query(PureOrg)
    .filter(PureOrg.pure_uuid == record_org_pure_uuid)
    .one_or_none()
  )

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

    # We will likely encounter integrity constraint violations if we have not
    # loaded this pub record previously:
    db_pub = find_db_pub(pure_pub['pure_uuid'])
    if db_pub is None:
      continue

    # For all orgs associated with this publication, a map of their pure_uuid's
    # to their full records. Needed to populate PubPersonPureOrg.
    all_pub_orgs = {}

    # Map of external org names to their full records. Needed to match
    # external persons to their orgs.
    external_pub_orgs = {}

    for external_org in pure_pub['associated_external_organisations']:
      external_pub_orgs[external_org['name_en']] = external_org
      all_pub_orgs[external_org['pure_uuid']] = external_org

    for org_assoc in pure_pub['organisation_associations']:
      org = org_assoc['organisation']
      all_pub_orgs[org['pure_uuid']] = org

    for person_assoc in pure_pub['person_associations']:
      # Ignoring these for now, because this info seems repeated elsewhere.
      # TODO: Verify the above, probably with Lars.
      #if 'organisation_associations' in person_assoc:
      #  for org_assoc in person_assoc['organisation_associations']:

      # For some strange reason, some person_assoc's do not contain person records:
      if 'person' not in person_assoc:
        continue
      pure_person = person_assoc['person']
      db_person = find_db_person(pure_person['pure_uuid'])
      if db_person is None:
        # This should never happen:
        print("pub-associated person missing from experts db:")
        pp.pprint(pure_person)
        continue

      db_pub_person = find_db_pub_person(db_person.uuid, db_pub.uuid)
      if db_pub_person is not None:
        # Should never happen, but just in case:
        print('pub-person association already exists in experts db: person_uuid: {}, pub_uuid: {}'.format(db_person.uuid, db_pub.uuid))
      else:
        db_pub_person = PubPerson(
          person_uuid = db_person.uuid,
          emplid = db_person.emplid,
          person_ordinal = person_assoc['ordinal'],
          person_role = person_assoc['person_role'],
          person_pure_internal = db_person.pure_internal,
          first_name = person_assoc['first_name'],
          last_name = person_assoc['last_name'],
          pub_uuid = db_pub.uuid
        )
        session.add(db_pub_person)

      if db_person.pure_internal == 'N' and person_assoc['external_organisation'] is not None:
        external_org_name = person_assoc['external_organisation']
        if external_org_name in external_pub_orgs:
          external_org = external_pub_orgs[external_org_name]
          db_org = find_db_org(external_org['pure_uuid'])
          if db_org is not None:
            db_person_pure_org = find_db_person_pure_org(db_person.uuid, db_org.pure_uuid)
            if db_person_pure_org is None:
              db_person_pure_org = PersonPureOrg(
                person_uuid = db_person.uuid,
                pure_org_uuid = db_org.pure_uuid
              )
              session.add(db_person_pure_org)
    
            # External persons will also have only one pub-org association, so may as well
            # take add it here:
            db_pub_person_pure_org = find_db_pub_person_pure_org(db_pub.uuid, db_person.uuid, db_org.pure_uuid)
            if db_pub_person_pure_org is not None:
              # Should never happen, but just in case:
              print('pub-person-pure_org association already exists in experts db: pub_uuid: {}, person_uuid: {}, pure_org_uuid: {}'.format(db_pub.uuid, db_person.uuid, db_org.pure_uuid))
            else:
              db_pub_person_pure_org = PubPersonPureOrg(
                pub_uuid = db_pub.uuid,
                person_uuid = db_person.uuid,
                pure_org_uuid = db_org.pure_uuid
              )
              session.add(db_pub_person_pure_org)

        # Go to the next person_assoc, because we should have no other
        # data for an external person:
        continue

      # Org info is often repeated for internal persons, so:
      orgs_seen = {}

      for org_assoc in person_assoc['person']['organisation_associations']:
        record_org = org_assoc['organisation']
        if record_org['pure_uuid'] in orgs_seen:
          continue
        db_org = find_db_org(record_org['pure_uuid'])
        if db_org is None:
          continue
        orgs_seen[db_org.pure_uuid] = record_org

      for staff_org_assoc in person_assoc['person']['staff_organisation_associations']:
        record_org = staff_org_assoc['organisation']
        if record_org['pure_uuid'] in orgs_seen:
          continue
        db_org = find_db_org(record_org['pure_uuid'])
        if db_org is None:
          continue
        orgs_seen[db_org.pure_uuid] = record_org

      for org_uuid in orgs_seen:

        db_person_pure_org = find_db_person_pure_org(db_person.uuid, org_uuid)
        if db_person_pure_org is None:
          db_person_pure_org = PersonPureOrg(
            person_uuid = db_person.uuid,
            pure_org_uuid = org_uuid
          )
          session.add(db_person_pure_org)

        # For these, make sure the organisation is actually associated with the pub:
        if org_uuid not in all_pub_orgs:
          continue
        db_pub_person_pure_org = find_db_pub_person_pure_org(db_pub.uuid, db_person.uuid, org_uuid)
        if db_pub_person_pure_org is not None:
          # Should never happen, but just in case:
          print('pub-person-pure_org association already exists in experts db: pub_uuid: {}, person_uuid: {}, pub_uuid: {}'.format(db_pub.uuid, db_person.uuid, db_pub.uuid))
        else:
          db_pub_person_pure_org = PubPersonPureOrg(
            pub_uuid = db_pub.uuid,
            person_uuid = db_person.uuid,
            pure_org_uuid = org_uuid
          )
          session.add(db_pub_person_pure_org)

  session.commit()
