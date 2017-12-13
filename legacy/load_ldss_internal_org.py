# One-off to load quirky LDSS data into PureInternalOrg.

from models import PureInternalOrg
from sqlalchemy import func

import db
session = db.session('hotel')

max_id = session.query(func.max(PureInternalOrg.id)).scalar()
pure_internal_org = PureInternalOrg(
  id = max_id + 1,
  parent_id = 22,
  pure_uuid = 'a6bfaa1e-53d6-49ae-952b-62b78aef7c70',
  pure_id = None,
  name_en = 'Library Data & Student Success'
)
session.add(pure_internal_org)
session.commit()
