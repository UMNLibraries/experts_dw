# One-off to load quirky LDSS data into PureInternalOrg.

from models import PureInternalOrg
from sqlalchemy import func

import db
session = db.session('hotel')

pure_orgs = [
  {
    'pure_uuid': '9b529085-6db5-4cda-9c2c-ad4145ec441e',
    'pure_id': 'MNDRIVETRANSDISC',
    'parent_pure_uuid': '13cffe90-f5c3-4b93-8a14-f74c358d4e93',
    'parent_pure_id': 'MNDRIVE',
    'pure_internal': 'Y',
    'type': 'initiative',
    'name_en': 'Transdisciplinary Research (MnDRIVE)',
  },
  {
    'pure_uuid': 'e992d5ba-5d4f-4d87-8dba-6381b02afaa6',
    'pure_id': 'MNDRIVEROBOT',
    'parent_pure_uuid': '13cffe90-f5c3-4b93-8a14-f74c358d4e93',
    'parent_pure_id': 'MNDRIVE',
    'pure_internal': 'Y',
    'type': 'initiative',
    'name_en': 'Robotics (MnDRIVE)',
  },
  {
    'pure_uuid': '2934748e-5035-4086-b2fa-a14d554b87c1',
    'pure_id': 'MNDRIVEINFRA',
    'parent_pure_uuid': '13cffe90-f5c3-4b93-8a14-f74c358d4e93',
    'parent_pure_id': 'MNDRIVE',
    'pure_internal': 'Y',   
    'type': 'initiative',
    'name_en': 'Infrastructure (MnDRIVE)',
  },
  {
    'pure_uuid': '0aff1121-7a80-4dc1-9426-5cf6456c0626',
    'pure_id': 'MNDRIVEINFORM',
    'parent_pure_uuid': '13cffe90-f5c3-4b93-8a14-f74c358d4e93',
    'parent_pure_id': 'MNDRIVE',
    'pure_internal': 'Y',
    'type': 'initiative',
    'name_en': 'Informatics (MnDRIVE)',                                               
  },
  {
    'pure_uuid': 'ca5c08a2-86c3-4ed7-8265-6b37554907fd',
    'pure_id': 'MNDRIVEFOOD',
    'parent_pure_uuid': '13cffe90-f5c3-4b93-8a14-f74c358d4e93',
    'parent_pure_id': 'MNDRIVE',
    'pure_internal': 'Y',
    'type': 'initiative',
    'name_en': 'Global Food (MnDRIVE)',                                               
  },
  {
    'pure_uuid': 'b44e82a4-8007-4ea2-a1e4-d65403608748',
    'pure_id': 'MNDRIVEENV',
    'parent_pure_uuid': '13cffe90-f5c3-4b93-8a14-f74c358d4e93',
    'parent_pure_id': 'MNDRIVE',
    'pure_internal': 'Y',
    'type': 'initiative',
    'name_en': 'Environment (MnDRIVE)',
  },
  {
    'pure_uuid': '533628bb-2f32-4d5a-b7e6-1473277a5f0d',
    'pure_id': 'MNDRIVEBRAIN',
    'parent_pure_uuid': '13cffe90-f5c3-4b93-8a14-f74c358d4e93',
    'parent_pure_id': 'MNDRIVE',
    'pure_internal': 'Y',
    'type': 'initiative',
    'name_en': 'Brain Conditions (MnDRIVE)',                                              
  },
]

for pure_org in pure_orgs:
  max_id = session.query(func.max(PureInternalOrg.id)).scalar()
  pure_internal_org = PureInternalOrg(
    id = max_id + 1,
    parent_id = 275,
    pure_uuid = pure_org['pure_uuid'],
    pure_id = pure_org['pure_id'],
    name_en = pure_org['name_en']
  )
  session.add(pure_internal_org)
session.commit()

