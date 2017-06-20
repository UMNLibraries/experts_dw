import env
from pureapi import client, parser
from models import Person

import db
session = db.session('hotel')

params = { 
  'window.size': 20,
  'namespaces': 'remove',
  'rendering': 'xml_long',
}
for response in client.get_all('person', params):
  for record in parser.records(response.text):
    pure_person = parser.person(record)
    db_person = (
      session.query(Person)
      .filter(Person.emplid == pure_person['emplid'])
      .one_or_none()
    )
    if db_person is not None:
      db_person.pure_uuid = pure_person['pure_uuid']
      db_person.scopus_id = pure_person['scopus_id']
      db_person.hindex = pure_person['hindex']
    else:
      print(pure_person)
  session.commit()
