# One-off to update the person_scival_id master dataset table with UUIDs.

import db
session = db.session('hotel')

from models import MdsPersonScivalId, MdsPersonEmplid

for person_scival_id in session.query(MdsPersonScivalId).all():
  person_emplid = (
    session.query(MdsPersonEmplid)
    .filter(MdsPersonEmplid.emplid == person_scival_id.emplid)
    .one_or_none()
  )
  person_scival_id.uuid = person_emplid.uuid

session.commit()
