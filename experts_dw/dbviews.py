import sys
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

poi_columns =  ', '.join([
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

employee_job_columns =  ', '.join([
    'EMPLID',
    'EMPL_RCDNO',
    'EFFDT',
    'EFFSEQ',
    'NAME',
    'POSITION_NBR',
    'JOBCODE',
    'JOBCODE_DESCR',
    'JOB_INDICATOR', # Do we even use this? Not in ps_dwhr_poi_uns.
    'EMPL_STATUS',
    'PAYGROUP',
    'DEPTID',
    'DEPTID_DESCR',
    'UM_JOBCODE_GROUP', # Do we even use this? Not in ps_dwhr_poi_uns.
    'UM_COLLEGE',
    'UM_COLLEGE_DESCR',
    'UM_CAMPUS',
    'UM_CAMPUS_DESCR',
    'RRC',
    'UM_ZDEPTID',
    'UM_ZDEPTID_DESCR',
    'STATUS_FLG',
    'JOB_TERMINATED', # Not in ps_dwhr_poi_uns.
    'LAST_DATE_WORKED', # Not in ps_dwhr_poi_uns.
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
    'UM_CAMPUS_DESCR',
    'UM_ZDEPTID',
    'UM_ZDEPTID_DESCR',
    'STATUS_FLG',
])

poi_job_columns =  ', '.join([
    'EMPLID',
    'EMPL_RCDNO',
    'EFFDT',
    'EFFSEQ',
    'NAME',
    'POSITION_NBR',
    'JOBCODE',
    'JOBCODE_DESCR',
    'EMPL_STATUS',
    'PAYGROUP',
    'DEPTID',
    'DEPTID_DESCR',
    'UM_COLLEGE',
    'UM_COLLEGE_DESCR',
    'UM_CAMPUS',
    'UM_CAMPUS_DESCR',
    'RRC',
    'UM_ZDEPTID',
    'UM_ZDEPTID_DESCR',
    'STATUS_FLG',
    'JOB_ENTRY_DT',
    'POSITION_ENTRY_DT',
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

poi_ps_dwhr_poi_uns_columns = ', '.join([
    'j.emplid',
    'j.name',
    'j.jobcode',
    'j.jobcode_descr',
    'j.empl_status',
    'j.paygroup',
    'j.um_college',
    'j.um_college_descr',
    'j.rrc',
    'j.status_flg',
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
    'j.job_indicator', # Do we even use this? Not in ps_dwhr_poi_uns.
    'j.empl_status',
    'j.paygroup',
    'j.deptid',
    'j.deptid_descr',
    'j.um_jobcode_group', # Do we even use this? Not in ps_dwhr_poi_uns.
    'j.um_college',
    'j.um_college_descr',
    'j.um_campus',
    'j.um_campus_descr',
    'j.rrc', # experts_data: as campus
    'j.um_zdeptid',
    'j.um_zdeptid_descr',
    'j.status_flg',
    'j.job_terminated', # Not in ps_dwhr_poi_uns.
    'j.last_date_worked', # Not in ps_dwhr_poi_uns.
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
    'um_campus_descr',
    'um_zdeptid',
    'um_zdeptid_descr',
    'status_flg',
])

poi_job_ps_dwhr_poi_uns_columns = ', '.join([
    'j.emplid',
    'to_char(j.empl_rcdno) AS empl_rcdno',
    'j.effdt',
    'j.effseq',
    'j.name',
    'j.position_nbr',
    'j.jobcode',
    'j.jobcode_descr',
    'j.empl_status',
    'j.paygroup',
    'j.deptid',
    'j.deptid_descr',
    'j.um_college',
    'j.um_college_descr',
    'j.um_campus',
    'j.um_campus_descr',
    'j.rrc',
    'j.um_zdeptid',
    'j.um_zdeptid_descr',
    'j.status_flg',
    'j.job_entry_dt',
    'j.position_entry_dt',
])

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
  AND paygroup != 'PLH' -- Under 9, Stu Hrly, Short Term
  AND empl_class != 'FTD' -- (Fac - Temp/Duluth Non-Reg)
  AND um_college NOT IN (
    {um_colleges_to_exclude}
  )
'''

affiliate_common_restrictions = f'''
  AND poi_type = '00012'
  AND um_college NOT IN (
    {um_colleges_to_exclude}
  )
  AND (
    (um_affil_relation IN ('9401A','9402A','9403A'))
    OR
    (deptid IN (SELECT deptid FROM pure_eligible_affiliate_dept)
      AND um_affil_relation in (
        '9701',
        '9702',
        '9743', -- Is this a mistake? Was this meant to be 9703 instead?
        -- David Naughton mistakenly and indirectly added these last three jobcodes. Should we remove these?
        '9703',
        '9742R6',
        '9742R7',
        '9755'
      )
    )
    OR
    (um_affil_relation IN ('9401','9402','9403') AND um_college = 'TMED')
  )
'''

poi_common_restrictions = f'''
  AND j.action_reason <> 'EIE' -- Entered in Error
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
    JOIN pure_eligible_employee_jobcode jc
      ON j.jobcode = jc.jobcode
  WHERE empl_status IN ('A','L','P','W')
  AND j.status_flg = 'C' -- current
  {employee_common_restrictions}
)'''

pure_eligible_affiliate_view = f'''
CREATE OR REPLACE FORCE EDITIONABLE VIEW EXPERT.PURE_ELIGIBLE_AFFILIATE (
  {affiliate_columns}
) AS (
  SELECT DISTINCT {affiliate_ps_dwhr_um_affiliates_columns}
  FROM ps_dwhr_um_affiliates@dweprd.oit a
  WHERE status = 'A' -- active
  AND status_flg = 'C' -- current
  {affiliate_common_restrictions}
)'''

pure_eligible_poi_view = f'''
CREATE OR REPLACE EDITIONABLE VIEW EXPERT.PURE_ELIGIBLE_POI (
  {poi_columns}
) AS (
  SELECT DISTINCT {poi_ps_dwhr_poi_uns_columns}
  FROM ps_dwhr_poi_uns@dweprd.oit j
  JOIN pure_eligible_poi_jobcode jc ON j.jobcode = jc.jobcode
  WHERE empl_status = 'A'
  AND j.status_flg = 'C'
  {poi_common_restrictions}
)'''

pure_eligible_employee_job_view = f'''
CREATE OR REPLACE FORCE EDITIONABLE VIEW EXPERT.PURE_ELIGIBLE_EMPLOYEE_JOB (
  {employee_job_columns}
) AS (
  SELECT DISTINCT {employee_job_ps_dwhr_job_columns}
  FROM ps_dwhr_job@dweprd.oit j
    JOIN pure_eligible_employee_jobcode jc
      ON j.jobcode = jc.jobcode
  WHERE j.status_flg IN ('C','H') -- current or historical. We exclude F, future.
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

pure_eligible_poi_job_view = f'''
CREATE OR REPLACE FORCE EDITIONABLE VIEW EXPERT.PURE_ELIGIBLE_POI_JOB (
  {poi_job_columns}
) AS (
  SELECT DISTINCT {poi_job_ps_dwhr_poi_uns_columns}
  FROM ps_dwhr_poi_uns@dweprd.oit j
  JOIN pure_eligible_poi_jobcode jc ON j.jobcode = jc.jobcode
  WHERE status_flg IN ('C','H') -- current or historical. We exclude F, future.
  {poi_common_restrictions}
)'''

pure_eligible_graduate_program_view = f'''
CREATE OR REPLACE FORCE EDITIONABLE VIEW EXPERT.PURE_ELIGIBLE_GRADUATE_PROGRAM (STUDENT_ORG_ASSOCIATION_ID, PERSON_ID, PERIOD_START_DATE, PERIOD_END_DATE, NAME, ORG_ID, DEPTID, DEPTID_DESCR, STATUS, PS_DESCR, AFFILIATION_ID, EMAIL_ADDRESS) AS
WITH period_start AS (
  SELECT
    stix.emplid,
    stix.acad_career,
    stix.institution,
    stix.um_acad_plan_prima,
    MIN(term.term_begin_dt) AS start_date
  FROM ps_dwsa_stix_1223_pr@dweprd.oit stix
  JOIN ps_dwsa_prog_dtl@dweprd.oit prog
    ON  prog.emplid         = stix.emplid
    AND prog.acad_career    = stix.acad_career
    AND prog.institution    = stix.institution
    AND prog.acad_plan      = stix.um_acad_plan_prima
    AND prog.prog_status    = 'AC'
  JOIN cs_ps_term_tbl@dweprd.oit term
    ON  term.institution = prog.institution
    AND term.acad_career = prog.acad_career
    AND term.strm        = prog.admit_term
  WHERE stix.level2 IN ('GRAD','PRFL')
  GROUP BY stix.emplid, stix.acad_career, stix.institution, stix.um_acad_plan_prima
),
program_status AS (
  SELECT
    stix.emplid,
    stix.acad_career,
    stix.institution,
    stix.um_acad_plan_prima,
    prog.prog_status,
    CASE prog.prog_status
      WHEN 'CM' THEN 1 -- Completed Program
      WHEN 'CN' THEN 2 -- Cancelled
      WHEN 'DC' THEN 3 -- Discontinued
      WHEN 'DE' THEN 4 -- Deceased
      WHEN 'DM' THEN 5 -- Dismissed
      ELSE 9
      -- Other states:
      -- AC: Active in Program
      -- AD: Admitted
      -- AP: Applicant
      -- LA: Leave of Absence
      -- PM: Prematriculant
      -- SP: Suspended
      -- WT: Waitlisted
    END AS prog_status_rank,
    prog.ps_descr, -- program status description
    prog.effdt
  FROM ps_dwsa_stix_1223_pr@dweprd.oit stix
  JOIN ps_dwsa_prog_dtl@dweprd.oit prog
    ON  prog.emplid            = stix.emplid
    AND prog.acad_career       = stix.acad_career
    AND prog.institution       = stix.institution
    AND prog.acad_plan         = stix.um_acad_plan_prima
    AND prog.curr_record       = 'Y'
  WHERE stix.level2 IN ('GRAD','PRFL')
),
program_status_ranked AS (
  SELECT
    emplid,
    acad_career,
    institution,
    um_acad_plan_prima,
    prog_status,
    prog_status_rank,
    ps_descr,
    effdt,
    ROW_NUMBER() OVER (
      PARTITION BY
        emplid,
        acad_career,
        institution,
        um_acad_plan_prima
      ORDER BY prog_status_rank, effdt
    ) AS row_number
  FROM program_status
),
period_end AS (
  SELECT
    emplid,
    acad_career,
    institution,
    um_acad_plan_prima,
    prog_status,
    ps_descr,
    CASE
      WHEN prog_status_rank < 9 THEN effdt
      ELSE NULL
    END AS end_date
  FROM program_status_ranked
  WHERE row_number = 1
),
pure_academic_program_org AS (
  SELECT pure_id
  FROM pure_org
  WHERE pure_internal = 'Y'
  AND type = 'academic plan'
)
SELECT
  'autoid:' || stix.emplid || '-' || stix.um_acad_plan_prima || '-' || stix.degree || '-' || TO_CHAR(period_start.start_date, 'YYYY-MM-DD') AS student_org_association_id,
  stix.emplid AS person_id,
  period_start.start_date AS period_start_date,
  period_end.end_date AS period_end_date,
  stix.name, -- Use for demographic data? Or maybe just testing/troubleshooting.
  stix.um_acad_plan_prima AS org_id, -- The "Source ID" for academic plan organisations in Pure.
  stix.deptid, -- Use to verify existence of Pure parent org.
  stix.deptid_descr, -- Use for error reporting in case of missing Pure parent org.
  period_end.prog_status as status, -- We use this code in the URI of the "Student Registration status" classification scheme in Pure.
  period_end.ps_descr, -- We use this as the term in the above classification scheme.
  stix.degree AS affiliation_id, -- We use this code in the URI of the "Student types" classification scheme in Pure.
  CASE
    WHEN demog.um_dirc_exclude IN (
      '5', -- Suppress All Information - TOTAL SUPPRESSION
      '6', -- Suppress Phone, Address, Email - DIRECTORY SUPPRESSION
      NULL -- Default to NULL if we have no directory suppression value.
    ) THEN NULL
    ELSE demog.emailid_1
  END AS email_address
FROM ps_dwsa_stix_1223_pr@dweprd.oit stix
JOIN pure_academic_program_org papo
  ON stix.um_acad_plan_prima = papo.pure_id
JOIN period_start
  ON  period_start.emplid             = stix.emplid
  AND period_start.acad_career        = stix.acad_career
  AND period_start.institution        = stix.institution
  AND period_start.um_acad_plan_prima = stix.um_acad_plan_prima
JOIN period_end
  ON  period_end.emplid             = stix.emplid
  AND period_end.acad_career        = stix.acad_career
  AND period_end.institution        = stix.institution
  AND period_end.um_acad_plan_prima = stix.um_acad_plan_prima
LEFT OUTER JOIN ps_dwsa_demo_addr_rt@dweprd.oit demog
  ON demog.emplid = stix.emplid
WHERE stix.level2 IN ('GRAD','PRFL')
  -- The following are all part of our composite PK, so ensure they're not null:
  AND stix.emplid IS NOT NULL
  AND stix.um_acad_plan_prima IS NOT NULL
  AND stix.degree IS NOT NULL
  AND period_start.start_date IS NOT NULL
ORDER BY stix.emplid
'''

pure_eligible_demographics = f'''
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
) AS SELECT DISTINCT
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
  CASE
    -- For students who have directory suppression enabled,
    -- set their email addresses to NULL, so they won't be
    -- publicly displayed.
    WHEN sa.um_dirc_exclude = 6 THEN NULL -- 6 = directory suppression
    ELSE da.instl_email_addr
  END AS instl_email_addr,
  da.tenure_flag,
  da.tenure_track_flag,
  da.primary_empl_rcdno
FROM pure_eligible_person_chng_hst p
  JOIN ps_dwhr_demo_addr_vw@dweprd.oit da
    ON p.emplid = da.emplid
  LEFT JOIN ps_dwsa_demo_addr_rt@dweprd.oit sa
    ON p.emplid = sa.emplid
'''

pure_eligible_person = f'''
CREATE OR REPLACE FORCE EDITIONABLE VIEW EXPERT.PURE_ELIGIBLE_PERSON (
  EMPLID
) AS (
  SELECT emplid
  FROM pure_eligible_affiliate
  UNION
  SELECT emplid
  FROM pure_eligible_employee
  UNION
  SELECT emplid
  FROM pure_eligible_poi
  UNION
  SELECT person_id
  FROM pure_eligible_graduate_program
)'''

def create_view_pure_eligible_demographics(session):
    result = session.execute(
        sqlparse.format(pure_eligible_demographics, reindent=True)
    )
    session.commit()
    return result

def create_view_pure_eligible_person(session):
    result = session.execute(
        sqlparse.format(pure_eligible_person, reindent=True)
    )
    session.commit()
    return result

# Defines the criteria for a person's graduate program to be Pure-eligible.
def create_view_pure_eligible_graduate_program(session):
    result = session.execute(
        sqlparse.format(pure_eligible_graduate_program_view, reindent=True)
    )
    session.commit()
    return result

# Defines the criteria for an affiliate person to be Pure-eligible.
def create_view_pure_eligible_affiliate(session):
    result = session.execute(
        sqlparse.format(pure_eligible_affiliate_view, reindent=True)
    )
    session.commit()
    return result

# Defines the criteria for a POI person to be Pure-eligible.
def create_view_pure_eligible_poi(session):
    result = session.execute(
        sqlparse.format(pure_eligible_poi_view, reindent=True)
    )
    session.commit()
    return result

# Defines the criteria for an employee person to be Pure-eligible.
def create_view_pure_eligible_employee(session):
    result = session.execute(
        sqlparse.format(pure_eligible_employee_view, reindent=True)
    )
    session.commit()
    return result

# All Pure-eligible jobs ever held by a Pure-eligible affiliate employee.
def create_view_pure_eligible_affiliate_job(session):
    result = session.execute(
        sqlparse.format(pure_eligible_affiliate_job_view, reindent=True)
    )
    session.commit()
    return result

# Defines the criteria for a POI person to be Pure-eligible.
def create_view_pure_eligible_poi_job(session):
    result = session.execute(
        sqlparse.format(pure_eligible_poi_job_view, reindent=True)
    )
    session.commit()
    return result

# All Pure-eligible jobs ever held by a Pure-eligible employee.
def create_view_pure_eligible_employee_job(session):
    result = session.execute(
        sqlparse.format(pure_eligible_employee_job_view, reindent=True)
    )
    session.commit()
    return result
# Returns a list of view creation function names
def _view_creation_functions():
    return list(filter((lambda fn: fn.startswith('create_view_')), dir(sys.modules[__name__])))

# Convenience function to call all view creation functions in this module
def create_all_views(session):
    results = {}
    for fn in _view_creation_functions():
        results[fn] = getattr(sys.modules[__name__], fn)(session)
    return results
