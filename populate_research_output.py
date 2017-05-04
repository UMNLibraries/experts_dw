import pure_api_client as client
import pure_api_response_parser as parser
from models import ResearchOutput, Person, ResearchOutputPersonMap

import db
session = db.session('hotel')

params = { 
  'window.size': 5,
  'namespaces': 'remove',
  'rendering': 'xml_long',
}
for response in client.get_all('publication', params):
  for record in parser.records(response.text):
    type = record.attrib['type']
    if type != 'stab:ContributionToJournalType':
      continue
    pure_research_output = parser.publication(record)
    #print(pure_research_output)
  break
#    db_person = (
#      session.query(Person)
#      .filter(Person.emplid == pure_person['emplid'])
#      .one_or_none()
#    )
#    if db_person is not None:
#      db_person.pure_uuid = pure_person['pure_uuid']
#      db_person.scopus_id = pure_person['scopus_id']
#      db_person.hindex = pure_person['hindex']
#    else:
#      print(pure_person)
#  session.commit()
