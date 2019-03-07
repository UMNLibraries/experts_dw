import sqlparse

employee_columns =  ', '.join([
    'EMPLID',
    'NAME',
    'JOBCODE',
    'JOBCODE_DESCR',
    'EMPL_STATUS',
    'PAYGROUP',
    'UM_COLLEGE',
    'UM_COLLEGE_DESCR',
    'RRC',
    'STATUS_FLG',
])

affiliate_columns =  ', '.join([
    'EMPLID',
    'NAME',
    'UM_AFFIL_RELATION',
    'DEPTID',
    'DEPTID_DESCR',
    'UM_COLLEGE',
    'UM_COLLEGE_DESCR',
    'UM_CAMPUS',
    'STATUS_FLG',
])

employee_job_columns =  ', '.join([
    'EMPLID',
    'EMPL_RCDNO',
    'EFFDT',
    'EFFSEQ',
    'NAME',
    'POSITION_NBR',
    'JOBCODE',
    'JOBCODE_DESCR',
    'JOB_INDICATOR',
    'EMPL_STATUS',
    'PAYGROUP',
    'DEPTID',
    'DEPTID_DESCR',
    'UM_JOBCODE_GROUP',
    'UM_COLLEGE',
    'UM_COLLEGE_DESCR',
    'RRC',
    'UM_ZDEPTID',
    'UM_ZDEPTID_DESCR',
    'STATUS_FLG',
    'JOB_TERMINATED',
    'LAST_DATE_WORKED',
    'JOB_ENTRY_DT',
    'POSITION_ENTRY_DT',
])

affiliate_job_columns =  ', '.join([
    'EMPLID',
    'NAME',
    'UM_AFFILIATE_ID',
    'EFFDT',
    'UM_AFFIL_RELATION',
    'TITLE',
    'DEPTID',
    'DEPTID_DESCR',
    'STATUS',
    'UM_COLLEGE',
    'UM_COLLEGE_DESCR',
    'UM_CAMPUS',
    'UM_ZDEPTID',
    'UM_ZDEPTID_DESCR',
    'STATUS_FLG',
])

employee_ps_dwhr_job_columns = ', '.join([
    'j.emplid',
    'j.name', # for testing
    'j.jobcode',
    'j.jobcode_descr',
    'j.empl_status',
    'j.paygroup',
    'j.um_college',
    'j.um_college_descr',
    'j.rrc', # experts_data: as campus
    'j.status_flg',
])

affiliate_ps_dwhr_um_affiliates_columns = ', '.join([
    'emplid',
    'name', # for testing
    'um_affil_relation', # experts_data: as jobcode
    'deptid',
    'deptid_descr',
    'um_college',
    'um_college_descr',
    'um_campus', # experts_data: as campus
    'status_flg',
])

employee_job_ps_dwhr_job_columns = ', '.join([
    'j.emplid',
    'to_char(j.empl_rcdno) AS empl_rcdno',
    'j.effdt',
    'j.effseq',
    'j.name', # for testing
    'j.position_nbr',
    'j.jobcode',
    'j.jobcode_descr',
    'j.job_indicator',
    'j.empl_status',
    'j.paygroup',
    'j.deptid',
    'j.deptid_descr',
    'j.um_jobcode_group',
    'j.um_college',
    'j.um_college_descr',
    'j.rrc', # experts_data: as campus
    'j.um_zdeptid',
    'j.um_zdeptid_descr',
    'j.status_flg',
    'j.job_terminated',
    'j.last_date_worked',
    'j.job_entry_dt',
    'j.position_entry_dt',
])

affiliate_job_ps_dwhr_um_affiliates_columns = ', '.join([
    'emplid',
    'name', # for testing
    'um_affiliate_id',
    'effdt',
    'um_affil_relation', # experts_data: as jobcode
    'title', # AKA jobcode_descr
    'deptid',
    'deptid_descr',
    'status',
    'um_college',
    'um_college_descr',
    'um_campus', # experts_data: as campus
    'um_zdeptid',
    'um_zdeptid_descr',
    'status_flg',
])

um_campuses_to_include = ', '.join(list(map(
    lambda x: f"'{x}'",
    [
        'TXXX',
        'DXXX',
    ]
)))

rrcs_to_exclude = ', '.join(list(map(
    lambda x: f"'{x}'",
    [
        'UMRXX',
        'UMCXX',
        'UMMXX',
    ]
)))

um_colleges_to_exclude = ', '.join(list(map(
    lambda x: f"'{x}'",
    [
        'CCSA', # UMC STU AFFAIR?ENROLLMENT MGMT
        'DATH', # UMD INTERCOLLEGIATE ATHLETICS
        'DAUS', # UMD Auxiliary Services
        'DCAS', # UMD Student Life
        'DCFO', # UMD Finance & Operations
        'DFAC', # UMD Facilities Management
        'MCER', # UMM External Relations
        'MCFI', # UMM-Finance/Operations
        'MCSA', # UMM-Student Affairs
        'TATH', # Intercollegiate Athletics
        'TAUD', # Internal Audit, Office of
        'TAUX', # Auxiliary Services
        'TBOY', # Boynton Health Service
        'TCAP', # Capital Planning/Project Mgmt
        'TCTR', # Controller's Office
        'TESU', # Did Jan miss this one?
        'TFAC', # Facilities Management
        'THSM', # University Health and Safety
        'TINS', # University Relations, Office of
        'TINF', # Information Technology
        'TOBR', # Board of Regents, Office of
        'TOGC', # General Counsel, Office of the
        'TOHR', # Human Resources, Office of
        'TPSR', # Planning, Space, and Real Estate
        'TSAF', # Public Safety
        'TSVC', # University Services
    ]
)))

employee_common_restrictions = f'''
  AND j.action_reason <> 'EIE' -- Entered in Error
  AND paygroup != 'PLH'
  AND empl_class != 'FTD' -- (Fac - Temp/Duluth Non-Reg)
  AND rrc NOT IN (
    {rrcs_to_exclude}
  )
  AND um_college NOT IN (
    {um_colleges_to_exclude}
  )
'''

affiliate_common_restrictions = f'''
  AND poi_type = '00012'
  AND (
    (um_affil_relation IN (SELECT jobcode FROM pure_eligible_affiliate_jobcode)) -- Affiliate-specific jobcodes, e.g., 9401A, 9402A, and 9403A
    OR
    (deptid IN (SELECT deptid FROM pure_eligible_affiliate_dept)) -- Include jobs only from eligible departments for all other jobcodes.
  )
  AND um_campus IN (
    {um_campuses_to_include}
  )
  AND um_college NOT IN (
    {um_colleges_to_exclude}
  )
'''

pure_eligible_employee_view = f'''
CREATE OR REPLACE FORCE EDITIONABLE VIEW EXPERT.PURE_ELIGIBLE_EMPLOYEE (
  {employee_columns}
) AS (
  SELECT DISTINCT {employee_ps_dwhr_job_columns}
  FROM ps_dwhr_job@dweprd.oit j
    JOIN pure_eligible_jobcode jc
      ON j.jobcode = jc.jobcode
  WHERE empl_status IN ('A','L','P','W')
  AND j.status_flg = 'C'
  {employee_common_restrictions}
)'''

pure_eligible_affiliate_view = f'''
CREATE OR REPLACE FORCE EDITIONABLE VIEW EXPERT.PURE_ELIGIBLE_AFFILIATE (
  {affiliate_columns}
) AS (
  SELECT DISTINCT {affiliate_ps_dwhr_um_affiliates_columns}
  FROM ps_dwhr_um_affiliates@dweprd.oit a
  WHERE status = 'A'
  AND status_flg = 'C'
  {affiliate_common_restrictions}
)'''

pure_eligible_employee_job_view = f'''
CREATE OR REPLACE FORCE EDITIONABLE VIEW EXPERT.PURE_ELIGIBLE_EMPLOYEE_JOB (
  {employee_job_columns}
) AS (
  SELECT DISTINCT {employee_job_ps_dwhr_job_columns}
  FROM ps_dwhr_job@dweprd.oit j
    JOIN pure_eligible_jobcode jc
      ON j.jobcode = jc.jobcode
  WHERE j.status_flg IN ('C','H')
  {employee_common_restrictions}
  AND emplid IN (SELECT emplid FROM pure_eligible_person_chng_hst)
)'''

pure_eligible_affiliate_job_view = f'''
CREATE OR REPLACE FORCE EDITIONABLE VIEW EXPERT.PURE_ELIGIBLE_AFFILIATE_JOB (
  {affiliate_job_columns}
) AS (
  SELECT DISTINCT {affiliate_job_ps_dwhr_um_affiliates_columns}
  FROM ps_dwhr_um_affiliates@dweprd.oit a
  WHERE status_flg IN ('C','H')
  {affiliate_common_restrictions}
  AND emplid IN (SELECT emplid FROM pure_eligible_person_chng_hst)
)'''

def create_pure_eligible_demographics(session):
    stmt = """
CREATE OR REPLACE FORCE EDITIONABLE VIEW EXPERT.PURE_ELIGIBLE_DEMOGRAPHICS (
  EMPLID,
  INTERNET_ID,
  NAME,
  LAST_NAME,
  FIRST_NAME,
  MIDDLE_INITIAL,
  NAME_SUFFIX,
  INSTL_EMAIL_ADDR,
  TENURE_FLAG,
  TENURE_TRACK_FLAG,
  PRIMARY_EMPL_RCDNO
) AS select distinct
  da.emplid,
  da.internet_id,
  da.name, -- for testing
  da.last_name,
  da.first_name,
  SUBSTR(da.middle_name, 1, 1) AS middle_initial,
  CASE
    WHEN da.name_suffix LIKE 'Jr%' THEN 'Jr'
    WHEN da.name_suffix LIKE 'Sr%' THEN 'Sr'
    WHEN da.name_suffix LIKE 'III%' THEN 'III'
    WHEN da.name_suffix LIKE 'II%' THEN 'II'
    WHEN da.name_suffix LIKE 'IV%' THEN 'IV'
    WHEN da.name_suffix LIKE 'V%' THEN 'V'
    ELSE ''
  END AS name_suffix,
  da.instl_email_addr,
  da.tenure_flag,
  da.tenure_track_flag,
  da.primary_empl_rcdno
FROM pure_eligible_person_chng_hst p
  JOIN ps_dwhr_demo_addr_vw@dweprd.oit da
    ON p.emplid = da.emplid
"""
    result = session.execute(stmt)
    session.commit()
    return result

def create_pure_eligible_person(session):
    stmt = """
CREATE OR REPLACE FORCE EDITIONABLE VIEW EXPERT.PURE_ELIGIBLE_PERSON (
  EMPLID
) AS (
  SELECT emplid
  FROM pure_eligible_affiliate
  UNION
  SELECT emplid
  FROM pure_eligible_employee
)"""
    result = session.execute(stmt)
    session.commit()
    return result

# Defines the criteria for an affiliate person to be Pure-eligible.
def create_pure_eligible_affiliate(session):
    result = session.execute(
        sqlparse.format(pure_eligible_affiliate_view, reindent=True)
    )
    session.commit()
    return result

# Defines the criteria for an employee person to be Pure-eligible.
def create_pure_eligible_employee(session):
    result = session.execute(
        sqlparse.format(pure_eligible_employee_view, reindent=True)
    )
    session.commit()
    return result

# All Pure-eligible jobs ever held by a Pure-eligible affiliate employee.
def create_pure_eligible_affiliate_job(session):
    result = session.execute(
        sqlparse.format(pure_eligible_affiliate_job_view, reindent=True)
    )
    session.commit()
    return result

# All Pure-eligible jobs ever held by a Pure-eligible employee.
def create_pure_eligible_employee_job(session):
    result = session.execute(
        sqlparse.format(pure_eligible_employee_job_view, reindent=True)
    )
    session.commit()
    return result
