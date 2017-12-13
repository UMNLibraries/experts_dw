# One-off to load persons, especially external persons, from publication records:
import env
from pureapi import client, parser
from models import Person

import db
session = db.session('hotel')

import uuid

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

    for person_association in pure_pub['person_associations']:
      # For some strange reason, some person_associaions do not contain person records:
      if 'person' not in person_association:
        continue
      pure_person = person_association['person']
      db_person = (
        session.query(Person)
        .filter(Person.pure_uuid == pure_person['pure_uuid'])
        .one_or_none()
      )
      if db_person is not None:
        # For now, skipping already-loaded persons:
        continue

      db_person = Person(
        uuid = str(uuid.uuid4()),
        pure_uuid = pure_person['pure_uuid'],
        first_name = pure_person['first_name'],
        last_name = pure_person['last_name'],
        scopus_id = pure_person['scopus_id'],
        pure_internal = pure_person['pure_internal'],
        pure_id = pure_person['pure_id'],
        emplid = pure_person['emplid'],
        internet_id = pure_person['internet_id'],
        hindex = pure_person['hindex'],
      )
      session.add(db_person)

    session.commit()
