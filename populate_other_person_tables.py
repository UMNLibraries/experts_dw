# One-off to populate person-related mds tables that do not need their own special procedures.

import db
c = db.engine('dwe').connect()
s = db.session('hotel')

from dwe_models import PsDwhrDemoAddr
#from models import MdsPerson
import models

ps_to_mds_map = {
  'instl_email_addr': 'MdsPersonInstlEmailAddr',
  'internet_id': 'MdsPersonInternetId',
  'first_name': 'MdsPersonFirstName',
  'middle_name': 'MdsPersonMiddleName',
  'last_name': 'MdsPersonLastName',
  'name_suffix': 'MdsPersonNameSuffix',
  'preferred_name': 'MdsPersonPreferredName',
  'primary_empl_rcdno': 'MdsPersonPrimaryEmplRcdno',
  'tenure_flag': 'MdsPersonTenureFlag',
  'tenure_track_flag': 'MdsPersonTenureTrackFlag',
}

columns = list(ps_to_mds_map.keys())
st = (
  'select da.emplid, ' +
  ', '.join(['da.' + column for column in columns]) +
  ' from ps_dwhr_demo_addr@dweprd.oit da join mds_person p on da.emplid = p.emplid'
)

result = s.execute(st)
for row in result:
  emplid = row['emplid']
  for column in columns:
    mds_class_name = ps_to_mds_map[column]
    mds_class = getattr(models, mds_class_name)
    mds_obj = (
      s.query(mds_class)
      .filter(mds_class.emplid == emplid)
      .order_by(mds_class.timestamp.desc())
      .one_or_none()
    )
    if (mds_obj == None):
      # TODO: Not sure use of column here will work!
      mds_obj = mds_class(column=row[column], 'emplid'=emplid)
      s.add(mds_obj)
    else:
      # For new, only adding new rows if none already exist.
      continue

s.commit()


#rows = result.fetchall()
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
