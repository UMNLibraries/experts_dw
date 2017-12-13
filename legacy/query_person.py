# One-off to test queries of the person master dataset table, assumed to be empty.

import db
session = db.session('hotel')

from models import MdsPerson

for person in session.query(MdsPerson).order_by(MdsPerson.uuid)[1:4]:
  print(person)
