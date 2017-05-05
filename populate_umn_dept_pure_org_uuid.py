# One-off to populate umn_dept_pure_org.pure_org_uuid, assumed to be empty.

import db
session = db.session('hotel')
from models import UmnDeptPureOrg, PureOrg

for umn_dept_pure_org in session.query(UmnDeptPureOrg).all():
  pure_org = (
    session.query(PureOrg)
    .filter(PureOrg.pure_id == umn_dept_pure_org.pure_org_id)
    .one_or_none()
  )
  if pure_org is not None:
    umn_dept_pure_org.pure_org_uuid = pure_org.pure_uuid
    session.add(umn_dept_pure_org)
  else:
    # Should never happen:
    print(umn_dept_pure_org)
session.commit()
