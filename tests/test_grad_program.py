import dotenv_switch.auto

import pytest

from experts_dw import db
from experts_dw.grad_program import current_year, \
    previous_year, \
    valid_year, \
    term_table_names, \
    latest_term_table_name, \
    pure_eligible_graduate_program_view_sql, \
    update_pure_eligible_graduate_program_view, \
    ExpertsDwGradProgramInvalidYearError

@pytest.fixture
def connection():
    with db.cx_oracle_connection() as connection:
        yield connection

@pytest.fixture
def cursor(connection):
    return connection.cursor()

def test_valid_year():
    assert valid_year('00')
    assert valid_year('22')
    assert not valid_year('bogus')

def test_previous_year():
    prev_year = previous_year()
    assert valid_year(prev_year)
    assert (int(current_year()) - int(prev_year)) == 1

def test_term_table_names():
    assert (term_table_names(year='22') == (
        'PS_DWSA_STIX_1229_PR',
        'PS_DWSA_STIX_1225',
        'PS_DWSA_STIX_1225_INT',
        'PS_DWSA_STIX_1223_PR',
    ))

    with pytest.raises(ExpertsDwGradProgramInvalidYearError):
        table_names = term_table_names(year='bogus')

def test_latest_term_table_name(cursor):
    assert latest_term_table_name(cursor) in term_table_names(year=current_year()) + term_table_names(year=previous_year())

def test_pure_eligible_graduate_program_view_sql():
    assert pure_eligible_graduate_program_view_sql('PS_DWSA_STIX_1229_PR') == f'''
CREATE OR REPLACE FORCE EDITIONABLE VIEW EXPERT.PURE_ELIGIBLE_GRADUATE_PROGRAM (STUDENT_ORG_ASSOCIATION_ID, PERSON_ID, PERIOD_START_DATE, PERIOD_END_DATE, NAME, ORG_ID, DEPTID, DEPTID_DESCR, STATUS, PS_DESCR, AFFILIATION_ID, EMAIL_ADDRESS) AS
WITH period_start AS (
  SELECT
    stix.emplid,
    stix.acad_career,
    stix.institution,
    stix.um_acad_plan_prima,
    MIN(term.term_begin_dt) AS start_date
  FROM PS_DWSA_STIX_1229_PR@dweprd.oit stix
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
  FROM PS_DWSA_STIX_1229_PR@dweprd.oit stix
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
FROM PS_DWSA_STIX_1229_PR@dweprd.oit stix
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
  AND (stix.degree IS NOT NULL AND stix.degree <> ' ')
  AND period_start.start_date IS NOT NULL
ORDER BY stix.emplid
    '''
