import datetime
from datetime import date
import functools
import re
from typing import Any, Callable, MutableMapping, Tuple, TypeVar, cast

import cx_Oracle

from experts_dw.cx_oracle_helpers import select_list_of_scalars
from experts_dw.exceptions import ExpertsDwException

term_table_prefix: str = 'PS_DWSA_STIX_1'
'''String preceding the two-digit year in all student term table names.'''

term_table_suffixes: Tuple[str] = ('9_PR','5','5_INT','3_PR')
'''Tuple of strings which may follow the two-digit year in all student term table names, in reverse chronological order.'''

def valid_year(year: str) -> bool:
    '''For the given ``year``, returns ``True`` or ``False`` according to its
    validity. Valid values are two-digit years between 00 and the current year, inclusive.'''
    return \
        re.match(r'^\d\d$', year) and \
        int(year) >= 0 and \
        int(year) <= int(current_year())

def current_year() -> str:
    '''Returns the current two-digit year.'''

    # The strftime call returns a two-digit year.
    return date.today().strftime('%y') 

def previous_year() -> str:
    '''Returns the previous two-digit year.'''

    # The [-2:] selects the last two elements of the array of characters,
    # giving us a two-digit year.
    return str((date.today().year - 1))[-2:]

class ExpertsDwGradProgramInvalidYearError(ValueError, ExpertsDwException):
    '''Raised when the given ``year`` is invalid for a student term table name.'''
    def __init__(self, year, *args, **kwargs):
        super().__init__(f'Invalid year "{year}" for a student term table name', *args, **kwargs)

F = TypeVar('F', bound=Callable[..., Any])

def validate_year(func: F) -> F:
    '''A decorator wrapper that validates the year component of a student term table name.

    Args:
        func: The function to be wrapped.

    Returns:
        The wrapped function.

    Raises:
        ExpertsDwGradProgramInvalidYearError
    '''
    @functools.wraps(func)
    def wrapper_validate_year(*args, **kwargs):
        if 'year' in kwargs and kwargs['year'] is not None:
            if not valid_year(kwargs['year']):
                raise ExpertsDwGradProgramInvalidYearError(kwargs['year'])
        else:
            kwargs['year'] = current_year()
        return func(*args, **kwargs)
    return cast(F, wrapper_validate_year)

@validate_year
def term_table_names(*, year : str = None) -> Tuple[str]:
    '''Returns a tuple of student term table names for the given ``year``.

    Args:
        year: A two-digit year. Default: current year.

    Returns:
        A tuple of student term table names.

    Raises:
        ExpertsDwGradProgramInvalidYearError
    '''
    return tuple(f'{term_table_prefix}{year}{suffix}' for suffix in term_table_suffixes)

def latest_term_table_name(cursor : cx_Oracle.Cursor) -> str:
    '''Returns the name of the latest student term table name which exists in the OIT Legacy Data Warehouse.

    Args:
        cursor: A database connection with access to the OIT Legacy Data Warehouse.

    Returns:
        The latest student term table name.
    '''

    existing_db_table_names = select_list_of_scalars(
       cursor,
       f"SELECT table_name FROM all_tables@dweprd.oit WHERE table_name LIKE '{term_table_prefix}%'",
    )
    return next(
        (table_name
            for table_name
            in term_table_names(year=current_year()) + term_table_names(year=previous_year())
            if table_name in existing_db_table_names
        ), None
    )

def pure_eligible_graduate_program_view_sql(term_table_name : str) -> str:
    '''Returns a string of SQL to create or replace a view of Pure-eligible graduate student program data using the given student term table name.

    Args:
        term_table_name: The name of a student term table.

    Returns:
        A string of SQL to create or replace a view of Pure-eligible graduate student program data.
    '''

    return f'''
CREATE OR REPLACE FORCE EDITIONABLE VIEW EXPERT.PURE_ELIGIBLE_GRADUATE_PROGRAM (STUDENT_ORG_ASSOCIATION_ID, PERSON_ID, PERIOD_START_DATE, PERIOD_END_DATE, NAME, ORG_ID, DEPTID, DEPTID_DESCR, STATUS, PS_DESCR, AFFILIATION_ID, EMAIL_ADDRESS) AS
WITH period_start AS (
  SELECT
    stix.emplid,
    stix.acad_career,
    stix.institution,
    stix.um_acad_plan_prima,
    MIN(term.term_begin_dt) AS start_date
  FROM {term_table_name}@dweprd.oit stix
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
  FROM {term_table_name}@dweprd.oit stix
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
FROM {term_table_name}@dweprd.oit stix
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

def update_pure_eligible_graduate_program_view(cursor : cx_Oracle.Cursor, term_table_name : str = None) -> None:
    '''Creates or replaces a view of Pure-eligible grad student program data.

    Args:
        cursor: A database connection with access to the OIT Legacy Data Warehouse.
        term_table_name: The name of a student term table. Default: the latest student term table name.
    '''

    term_table_name = latest_term_table_name(cursor) if term_table_name is None else term_table_name
    cursor.execute(pure_eligible_graduate_program_view_sql(term_table_name))
