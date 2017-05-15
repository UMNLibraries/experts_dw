import pure_api_client as client
import pure_api_response_parser as parser
from models import Pub, Person, PureOrg, PersonPureOrg

import db
session = db.session('hotel')

from datetime import date
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

    if not db_org_exists(pure_pub['owner_organisation']['pure_uuid']):
      continue

    db_pub = (
      session.query(Pub)
      .filter(Pub.pure_uuid == pure_pub['pure_uuid'])
      .one_or_none()
    )
    if db_pub is None:
      db_pub = Pub(
        uuid = str(uuid.uuid4()),
        pure_uuid = pure_pub['pure_uuid']
      )

    # Now we should have a db_pub. Add the rest of the fields:

    db_pub.owner_pure_org_uuid = pure_pub['owner_organisation']['pure_uuid']
    db_pub.scopus_id = pure_pub['scopus_id']
    db_pub.pmid = pure_pub['pmid']
    db_pub.doi = pure_pub['doi']
    db_pub.type = pure_pub['type']
    db_pub.title = pure_pub['title']
    db_pub.container_title = pure_pub['container_title']
    db_pub.issn = pure_pub['issn']
    db_pub.volume = pure_pub['volume']
    db_pub.issue = pure_pub['issue']
    db_pub.pages = pure_pub['pages']
    db_pub.citation_total = pure_pub['citation_total']

    # issued_parts: 0: year, 1: month, 2: day
    issued_parts = pure_pub['issued']['date_parts']
    db_pub.issued = date(issued_parts[0], issued_parts[1], issued_parts[2])
    db_pub.issued_precision = pure_pub['issued_precision']

    session.add(db_pub)

  session.commit()
