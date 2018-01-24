from . import db

session = db.session('hotel')

def create_pure_eligible_demog():
  stmt = """
CREATE OR REPLACE FORCE EDITIONABLE VIEW "EXPERT"."PURE_ELIGIBLE_DEMOG" (
  "EMPLID",
  "INTERNET_ID",
  "NAME",
  "LAST_NAME",
  "FIRST_NAME",
  "MIDDLE_INITIAL",
  "NAME_SUFFIX",
  "INSTL_EMAIL_ADDR",
  "TENURE_FLAG",
  "TENURE_TRACK_FLAG",
  "PRIMARY_EMPL_RCDNO"
) AS select distinct
  da.emplid,
  da.internet_id,
  da.name, -- for testing
  da.last_name,
  da.first_name,
  substr(da.middle_name, 1, 1) as middle_initial,
  case
    when da.name_suffix like 'Jr%' then 'Jr'
    when da.name_suffix like 'Sr%' then 'Sr'
    when da.name_suffix like 'III%' then 'III'
    when da.name_suffix like 'II%' then 'II'
    when da.name_suffix like 'IV%' then 'IV'
    when da.name_suffix like 'V%' then 'V'
    else ''
  end as name_suffix,
  da.instl_email_addr,
  da.tenure_flag,
  da.tenure_track_flag,
  da.primary_empl_rcdno
from pure_eligible_person_chng_hst p
  join ps_dwhr_demo_addr_vw@dweprd.oit da
    on p.emplid = da.emplid
"""
  result = session.execute(stmt)
  session.commit()
  return result

def create_pure_eligible_person():
  stmt = """
CREATE OR REPLACE FORCE EDITIONABLE VIEW "EXPERT"."PURE_ELIGIBLE_PERSON" (
  "EMPLID"
) AS (
  select emplid
  from pure_eligible_affiliate
  union
  select emplid
  from pure_eligible_employee
)"""
  result = session.execute(stmt)
  session.commit()
  return result

# Defines the criteria for an affiliate person to be Pure-eligible.
def create_pure_eligible_affiliate():
  stmt = """
CREATE OR REPLACE FORCE EDITIONABLE VIEW "EXPERT"."PURE_ELIGIBLE_AFFILIATE" (
  "EMPLID",
  "NAME",
  "UM_AFFIL_RELATION",
  "DEPTID",
  "DEPTID_DESCR",
  "UM_COLLEGE",
  "UM_COLLEGE_DESCR",
  "UM_CAMPUS",
  "STATUS_FLG"
) AS (
  select distinct
    emplid,
    name, -- for testing
    um_affil_relation, -- experts_data: as jobcode
    deptid,
    deptid_descr,
    um_college,
    um_college_descr,
    um_campus, -- experts_data: as campus
    status_flg
 from ps_dwhr_um_affiliates@dweprd.oit a
 where poi_type = '00012'
   and status = 'A'
   and status_flg = 'C'
   and (
     (
       um_affil_relation in -- jobcode criteria table
       (select jobcode from job_codes where pool = 'A')
     ) or (
       um_affil_relation in -- only affiliates in designated jobcodes AND departments
       (select jobcode from job_codes where pool = 'C')
       and deptid in (select deptid from affiliate_departments)
     )
   )
   and um_campus in (
     'TXXX',
     'DXXX'
   )
   and um_college not in (
     'DATH',
     'DCAS',
     'TATH',
     'TAUD',
     'TAUX',
     'TBOY',
     'TCAP',
     'TCTR',
     'TFAC',
     'TOGC',
     'THSM',
     'TINS',
     'TOBR',
     'TOHR',
     'TSVC'
   )
)"""
  result = session.execute(stmt)
  session.commit()
  return result

# Defines the criteria for an employee person to be Pure-eligible.
def create_pure_eligible_employee():
  stmt = """
CREATE OR REPLACE FORCE EDITIONABLE VIEW "EXPERT"."PURE_ELIGIBLE_EMPLOYEE" (
  "EMPLID",
  "NAME",
  "JOBCODE",
  "JOBCODE_DESCR",
  "EMPL_STATUS",
  "PAYGROUP",
  "UM_COLLEGE",
  "UM_COLLEGE_DESCR",
  "RRC",
  "STATUS_FLG"
) AS (
  select distinct
    j.emplid,
    j.name, -- for testing
    j.jobcode,
    j.jobcode_descr,
    j.empl_status,
    j.paygroup,
    j.um_college,
    j.um_college_descr,
    j.rrc, -- experts_data: as campus
    j.status_flg
  from ps_dwhr_job@dweprd.oit j
    join job_codes jc
      on j.jobcode = jc.jobcode
  where empl_status in (
    'A',
    'L',
    'P',
    'W'
  )
    and j.status_flg = 'C'
    and paygroup != 'PLH'
    and rrc not in (
      'UMRXX',
      'UMCXX',
      'UMMXX'
    )
    and um_college not in (
      'DATH',
      'DCAS',
      'TATH',
      'TAUD',
      'TAUX',
      'TBOY',
      'TCAP',
      'TCTR',
      'TFAC',
      'TOGC',
      'THSM',
      'TINS',
      'TOBR',
      'TOHR',
      'TSVC'
    )
)"""   
  result = session.execute(stmt)
  session.commit()
  return result

# All Pure-eligible jobs ever held by a Pure-eligible affiliate employee.
def create_pure_eligible_aff_job():
  stmt = """
CREATE OR REPLACE FORCE EDITIONABLE VIEW "EXPERT"."PURE_ELIGIBLE_AFF_JOB" (
  "EMPLID",
  "NAME",
  "UM_AFFILIATE_ID",
  "EFFDT",
  "UM_AFFIL_RELATION",
  "TITLE",
  "DEPTID",
  "DEPTID_DESCR",
  "STATUS",
  "UM_COLLEGE",
  "UM_COLLEGE_DESCR",
  "UM_CAMPUS",
  "UM_ZDEPTID",
  "UM_ZDEPTID_DESCR",
  "STATUS_FLG"
) AS select distinct
  emplid,
  name, -- for testing
  um_affiliate_id,
  effdt,
  um_affil_relation, -- experts_data: as jobcode
  title, -- AKA jobcode_descr
  deptid,
  deptid_descr,
  status,
  um_college,
  um_college_descr,
  um_campus, -- experts_data: as campus
  um_zdeptid,
  um_zdeptid_descr,
  status_flg
from ps_dwhr_um_affiliates@dweprd.oit a
where poi_type = '00012'
  and status_flg in ('C','H')
  and (
    (
      um_affil_relation in -- jobcode criteria table
        (select jobcode from job_codes where pool = 'A')
    ) or (
      um_affil_relation in -- only affiliates in designated jobcodes AND departments
        (select jobcode from job_codes where pool = 'C')
      and deptid in (select deptid from affiliate_departments)
    )
  )
  and um_campus in ('TXXX','DXXX')
  and um_college not in (
    'DATH',
    'DCAS',
    'TATH',
    'TAUD',
    'TAUX',
    'TBOY',
    'TCAP',
    'TCTR',
    'TFAC',
    'TOGC',
    'THSM',
    'TINS',
    'TOBR',
    'TOHR',
    'TSVC'
  )
  and emplid in (select emplid from pure_eligible_person_chng_hst)
"""   
  result = session.execute(stmt)
  session.commit()
  return result

# All Pure-eligible jobs ever held by a Pure-eligible employee.
def create_pure_eligible_emp_job():
  stmt = """
CREATE OR REPLACE FORCE EDITIONABLE VIEW "EXPERT"."PURE_ELIGIBLE_EMP_JOB" (
  "EMPLID",
  "EMPL_RCDNO",
  "EFFDT",
  "EFFSEQ",
  "NAME",
  "POSITION_NBR",
  "JOBCODE",
  "JOBCODE_DESCR",
  "JOB_INDICATOR",
  "EMPL_STATUS",
  "PAYGROUP",
  "DEPTID",
  "DEPTID_DESCR",
  "UM_JOBCODE_GROUP",
  "UM_COLLEGE",
  "UM_COLLEGE_DESCR",
  "RRC",
  "UM_ZDEPTID",
  "UM_ZDEPTID_DESCR",
  "STATUS_FLG",
  "JOB_TERMINATED",
  "LAST_DATE_WORKED",
  "JOB_ENTRY_DT",
  "POSITION_ENTRY_DT"
) AS (
  select distinct
    j.emplid,
    to_char(j.empl_rcdno) as empl_rcdno,
    j.effdt,
    j.effseq,
    j.name, -- for testing
    j.position_nbr,
    j.jobcode,
    j.jobcode_descr,
    j.job_indicator,
    j.empl_status,
    j.paygroup,
    j.deptid,
    j.deptid_descr,
    j.um_jobcode_group,
    j.um_college,
    j.um_college_descr,
    j.rrc, -- experts_data: as campus
    j.um_zdeptid,
    j.um_zdeptid_descr,
    j.status_flg,
    j.job_terminated,
    j.last_date_worked,
    j.job_entry_dt,
    j.position_entry_dt
    -- experts_data: least(j.job_entry_dt, j.position_entry_dt) as calculated_start_dt
  from ps_dwhr_job@dweprd.oit j
    join job_codes jc
      on j.jobcode = jc.jobcode
  where j.status_flg in ('C','H')
  and paygroup != 'PLH'
  and rrc not in (
    'UMRXX',
    'UMCXX',
    'UMMXX'
  )
  and um_college not in (
    'DATH',
    'DCAS',
    'TATH',
    'TAUD',
    'TAUX',
    'TBOY',
    'TCAP',
    'TCTR',
    'TFAC',
    'TOGC',
    'THSM',
    'TINS',
    'TOBR',
    'TOHR',
    'TSVC'
  )
  and emplid in (select emplid from pure_eligible_person_chng_hst)
)"""   
  result = session.execute(stmt)
  session.commit()
  return result
