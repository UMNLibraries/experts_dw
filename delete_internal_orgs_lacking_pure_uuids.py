# One-off to load quirky LDSS data into PureInternalOrg.

from models import PureInternalOrg
from sqlalchemy import func

import db
session = db.session('hotel')

# NOTE: Also deleted these from umn_dept_pure_org, because we have no pure_org with pure_org_id ZNVNNMA:
# umn_dept_id: 10770, umn_dept_name: AES Greenhouses, pure_org_uuid: None, pure_org_id: ZNVNNMA
# umn_dept_id: 10773, umn_dept_name: AES Ag Services, pure_org_uuid: None, pure_org_id: ZNVNNMA
# umn_dept_id: 10764, umn_dept_name: AES Administration Operations, pure_org_uuid: None, pure_org_id: ZNVNNMA

# id  pure_id     type        name_en                                  lft parent_id level rft tree_id
# 271 NNIWQIQRQ   department  Minnesota Agriculture Experiment Station 577 24        3     578 1   
# 24  ZNVNNMA     college     Minnesota Agriculture Experiment Station 576 1         2     579 1   
for id in [24, 271]:
  org = session.query(PureInternalOrg).filter(PureInternalOrg.id == id).one_or_none()
  if org is not None:
    session.delete(org)
  else:
    print(id)
session.commit()
