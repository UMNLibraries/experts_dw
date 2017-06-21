# One-off to test queries of dwe table ps_dwhr_demo_addr.

import db
conn = db.engine('dwe').connect()

from dwe_models import PsDwhrDemoAddr
from sqlalchemy.sql import select

s = select([PsDwhrDemoAddr])
result = conn.execute(s)
row = result.fetchone()
print(
  'emplid:', row['emplid'],
  '; instl_email_addr:', row['instl_email_addr'],
  '; internet_id:', row['internet_id'],
  '; first_name:', row['first_name'],
  '; middle_name:', row['middle_name'],
  '; last_name:', row['last_name'],
  '; name_suffix:', row['name_suffix'],
  '; preferred_name:', row['preferred_name'],
  '; primary_empl_rcdno:', row['primary_empl_rcdno'],
  '; tenure_flag:', row['tenure_flag'],
  '; tenure_track_flag:', row['tenure_track_flag'],
)
