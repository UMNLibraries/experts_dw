# One-off to test queries of the person master dataset table, assumed to be empty.

import db
session = db.session('hotel')

from models import MdsPersonLastName

last_name = (
  session.query(MdsPersonLastName)
  .filter(MdsPersonLastName.uuid == '001bd704-dcab-4891-bc95-337d6b046dda')
  .order_by(MdsPersonLastName.timestamp.desc())
  .one_or_none()
)
if (last_name != None):
  print(last_name)
else:
  print("No rows found.")

