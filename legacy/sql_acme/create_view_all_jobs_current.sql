create or replace view all_jobs_current as (
	select 
    "EMPLID",
    "EMPL_RCDNO",
    "NAME",
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
    "CAMPUS",
    "UM_ZDEPTID",
    "UM_ZDEPTID_DESCR",
    "STATUS_FLG",
    "RECORD_SOURCE",
    "JOB_ENTRY_DT",
    "POSITION_ENTRY_DT",
    "CALCULATED_START_DT"
	from (
		select * from employee_jobs_current
		union
		select * from affiliate_jobs_current
	) jobs
	where 1=1
		and campus not in (
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
