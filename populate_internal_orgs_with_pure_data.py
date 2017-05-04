# One-off to populate some tables with UMN-internal org data.

import pure_api_client as client
import pure_api_response_parser as parser
from models import PureOrg, PureInternalOrg
from sqlalchemy import func

import db
session = db.session('hotel')

params = { 
  'window.size': 20,
  'namespaces': 'remove',
  'rendering': 'xml_long',
}
for response in client.get_all('organisation', params):
  for record in parser.records(response.text):
    org = parser.organisation(record)
    #print(org)

    pure_org = PureOrg(
      pure_uuid = org['pure_uuid'],
      pure_id = org['pure_id'],
      parent_pure_uuid = org['parent_pure_uuid'],
      parent_pure_id = org['parent_pure_id'],
      pure_internal = org['pure_internal'],
      name_en = org['name_en'],
      name_variant_en = org['name_variant_en'],
      type = org['type'],
      url = org['url']
    )
    session.add(pure_org)

    if org['pure_id'] is not None:
      pure_internal_org = (
        session.query(PureInternalOrg)
        .filter(PureInternalOrg.pure_id == org['pure_id'])
        .one_or_none()
      )
      if pure_internal_org is not None:
        pure_internal_org.pure_uuid = org['pure_uuid']
        session.add(pure_internal_org)
      elif org['parent_pure_id'] is not None:
        parent_pure_internal_org = (
          session.query(PureInternalOrg)
          .filter(PureInternalOrg.pure_id == org['parent_pure_id'])
          .one_or_none()
        )
        if parent_pure_internal_org is not None:
          max_id = session.query(func.max(PureInternalOrg.id)).scalar()
          pure_internal_org = PureInternalOrg(
            id = max_id + 1,
            parent_id = parent_pure_internal_org.id,
            pure_uuid = org['pure_uuid'],
            pure_id = org['pure_id'],
            name_en = org['name_en']
          )
          session.add(pure_internal_org)
      else:
        print(org)
    else:
      print(org)

session.commit()
