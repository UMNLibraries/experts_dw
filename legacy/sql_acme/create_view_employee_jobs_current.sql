create or replace view employee_jobs_current as (
  select
    j.emplid,
    to_char(j.empl_rcdno) as empl_rcdno,
    j.name, -- for testing
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
    j.rrc as campus,
    j.um_zdeptid,
    j.um_zdeptid_descr,
    j.status_flg,
    'J' as record_source, -- J for ps_dwhr_job or A for ps_um_affiliates for source
    j.job_entry_dt,
    j.position_entry_dt,
    least(j.job_entry_dt, j.position_entry_dt) as calculated_start_dt
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
);
