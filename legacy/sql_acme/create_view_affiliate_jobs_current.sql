create or replace view affiliate_jobs_current as (
	select
		emplid,
    -- Previously used a random number as an artificial value, but that makes it impossible to diff temporal snapshots.
		-- to_char(trunc(dbms_random.value(11,99))) as empl_rcdno, -- generate a value that's unlikely to collide with empl_rcdnos from the jobs table
		'99' as empl_rcdno, -- use a value that's unlikely to collide with empl_rcdnos from the jobs table
		name, -- for testing
		um_affil_relation as jobcode,
		title, -- AKA jobcode_descr
		-- create an artificial indicator for job precedence so that ONE of these can be set as
		-- PRIMARY_EMPL_RCDNO in the local demographics table. 
		-- Need to sort on both the jobcode (um_affil_relation) AND empl_rcdno (um_affiliate_id) to
		-- get a unique ranking for people with mulitple affiliate appointments with the same jobcode. Get it?
		to_char(rank() over (partition by emplid order by um_affil_relation asc, um_affiliate_id asc)) as job_indicator,
		'' as empl_status, -- empl_status EQUIV?
		'' as paygroup, -- paygroup EQUIV?
		deptid,
		deptid_descr,
		'' as um_jobcode_group, -- um_jobcode_group EQUIV?
		um_college,
		um_college_descr,
		um_campus as campus,
		um_zdeptid,
		um_zdeptid_descr,
		status_flg,
		'A' as record_source, -- J for ps_dwhr_job or A for ps_um_affiliates for source
		null as job_entry_dt,
		null as position_entry_dt,
		null as calculated_start_dt
	from ps_dwhr_um_affiliates@dweprd.oit a
	where poi_type = '00012'
		and status = 'A'
		and status_flg = 'C'
		and
			 (
				(um_affil_relation in -- jobcode criteria table
					(select jobcode from job_codes where pool = 'A')
				)
				or
				(um_affil_relation in -- only affiliates in designated jobcodes AND departments
					(select jobcode from job_codes where pool = 'C')
				 and deptid in (select deptid from affiliate_departments)
				)
			)
		and um_campus in (
      'TXXX',
      'DXXX'
    )
		and um_college not in
    (
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
