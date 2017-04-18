# One-off to populate person-related mds tables that do not need their own special procedures.

import db
session = db.session('hotel')

import models
from models import MdsPersonEmplid

table_class_names = [
  'MdsPersonInstlEmailAddr',
  'MdsPersonInternetId',
  'MdsPersonFirstName',
  'MdsPersonMiddleName',
  'MdsPersonLastName',
  'MdsPersonNameSuffix',
  'MdsPersonPreferredName',
  'MdsPersonPrimaryEmplRcdno',
  'MdsPersonTenureFlag',
  'MdsPersonTenureTrackFlag',
]

for table_class_name in table_class_names:
  table = getattr(models, table_class_name)
  for row in session.query(table).all():
      person_emplid = (
        session.query(MdsPersonEmplid)
        .filter(MdsPersonEmplid.emplid == row.emplid)
        .one_or_none()
      )
      row.uuid = person_emplid.uuid

session.commit()
