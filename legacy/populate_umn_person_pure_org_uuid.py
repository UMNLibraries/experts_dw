# One-off to populate umn_person_pure_org.pure_org_uuid, assumed to be empty.

import db
session = db.session('hotel')
from models import UmnPersonPureOrg, PureOrg

for umn_person_pure_org in session.query(UmnPersonPureOrg).all():
  pure_org = (
    session.query(PureOrg)
    .filter(PureOrg.pure_id == umn_person_pure_org.pure_org_id)
    .one_or_none()
  )
  if pure_org is not None:
    umn_person_pure_org.pure_org_uuid = pure_org.pure_uuid
    session.add(umn_person_pure_org)
  else:
    # Should never happen:
    print(umn_person_pure_org)
session.commit()
