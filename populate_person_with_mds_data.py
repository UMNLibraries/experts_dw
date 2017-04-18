# One-off to populate person-related mds tables that do not need their own special procedures.

import db
session = db.session('hotel')

import models
from models import Person, MdsPerson, MdsPersonEmplid, MdsPersonInternetId, MdsPersonFirstName, MdsPersonLastName, MdsPersonScivalId

for mds_person in session.query(MdsPerson).all():
  mds_person_emplid = (
    session.query(MdsPersonEmplid)
    .filter(MdsPersonEmplid.uuid == mds_person.uuid)
    .one()
  )
  mds_person_internet_id = (
    session.query(MdsPersonInternetId)
    .filter(MdsPersonInternetId.uuid == mds_person.uuid)
    .one()
  )
  mds_person_first_name = (
    session.query(MdsPersonFirstName)
    .filter(MdsPersonFirstName.uuid == mds_person.uuid)
    .one()
  )
  mds_person_last_name = (
    session.query(MdsPersonLastName)
    .filter(MdsPersonLastName.uuid == mds_person.uuid)
    .one()
  )
  mds_person_scival_id = (
    session.query(MdsPersonScivalId)
    .filter(MdsPersonScivalId.uuid == mds_person.uuid)
    .one_or_none()
  )
  pure_id = mds_person_scival_id.scival_id if mds_person_scival_id else mds_person_emplid.emplid

  person = Person(
    uuid = mds_person.uuid,
    emplid = mds_person_emplid.emplid,
    internet_id = mds_person_internet_id.internet_id,
    first_name = mds_person_first_name.first_name,
    last_name = mds_person_last_name.last_name,
    pure_id = pure_id
  )
  session.add(person)

session.commit()
