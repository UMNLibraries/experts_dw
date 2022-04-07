# Experts Raw SQL as Strings
# Used in OIT to EDW Process
# String names were formerly descriptive function names in pugsql (removed)
# Process now uses experts_dw db module with cx_oracle
# March 2022

count_pure_eligible_persons_in_dept = """
    select count(distinct emplid) from (
      select emplid from pure_eligible_employee_job where deptid = :deptid
      union
      select emplid from pure_eligible_affiliate_job where deptid = :deptid
    )
    """

delete_obsolete_primary_jobs = """
    DELETE FROM pure_sync_staff_org_association ps
    WHERE ps.primary_association = 1
    AND ps.modified < (
      SELECT MAX(ps2.modified)
      FROM pure_sync_staff_org_association ps2
      WHERE ps2.primary_association = 1
      AND ps2.person_id = ps.person_id
    )
    """

insert_pure_eligible_employee_jobcode = """
    INSERT INTO pure_eligible_employee_jobcode
    (
      jobcode,
      jobcode_descr,
      pure_job_description,
      default_employed_as,
      default_staff_type,
      default_visibility,
      default_profiled,
      default_profiled_overrideable
    ) VALUES (
      :jobcode,
      :jobcode_descr,
      :pure_job_description,
      :default_employed_as,
      :default_staff_type,
      :default_visibility,
      :default_profiled,
      :default_profiled_overrideable
    )
    """

insert_pure_sync_person_data = """
    INSERT INTO pure_sync_person_data ps
    (
      ps.person_id,
      ps.first_name,
      ps.last_name,
      ps.postnominal,
      ps.emplid,
      ps.internet_id,
      ps.visibility,
      ps.profiled,
      ps.created,
      ps.modified
    )
    SELECT
      pss.person_id,
      pss.first_name,
      pss.last_name,
      pss.postnominal,
      pss.emplid,
      pss.internet_id,
      pss.visibility,
      pss.profiled,
      SYSDATE,
      SYSDATE
    FROM pure_sync_person_data_scratch pss
    LEFT OUTER JOIN pure_sync_person_data ps
    ON pss.person_id = ps.person_id
    WHERE ps.person_id IS NULL
    """

insert_pure_sync_staff_org_association = """
    INSERT INTO pure_sync_staff_org_association ps
    (
      ps.staff_org_association_id,
      ps.person_id,
      ps.period_start_date,
      ps.period_end_date,
      ps.org_id,
      ps.employment_type,
      ps.staff_type,
      ps.visibility,
      ps.primary_association,
      ps.job_description,
      ps.affiliation_id,
      ps.email_address,
      ps.created,
      ps.modified
    )
    SELECT
      pss.staff_org_association_id,
      pss.person_id,
      pss.period_start_date,
      pss.period_end_date,
      pss.org_id,
      pss.employment_type,
      pss.staff_type,
      pss.visibility,
      pss.primary_association,
      pss.job_description,
      pss.affiliation_id,
      pss.email_address,
      SYSDATE,
      SYSDATE
    FROM pure_sync_staff_org_association_scratch pss
    LEFT OUTER JOIN pure_sync_staff_org_association ps
    ON pss.staff_org_association_id = ps.staff_org_association_id
    WHERE ps.staff_org_association_id IS NULL
    """

insert_pure_sync_student_org_association = """
    INSERT INTO pure_sync_student_org_association ps
    (
      ps.student_org_association_id,
      ps.person_id,
      ps.period_start_date,
      ps.period_end_date,
      ps.org_id,
      ps.status,
      ps.affiliation_id,
      ps.student_type_description,
      ps.email_address,
      ps.created,
      ps.modified
    )
    SELECT
      pss.student_org_association_id,
      pss.person_id,
      pss.period_start_date,
      pss.period_end_date,
      pss.org_id,
      pss.status,
      pss.affiliation_id,
      pss.student_type_description,
      pss.email_address,
      SYSDATE,
      SYSDATE
    FROM pure_sync_student_org_association_scratch pss
    LEFT OUTER JOIN pure_sync_student_org_association ps
    ON pss.student_org_association_id = ps.student_org_association_id
    WHERE ps.student_org_association_id IS NULL
    """

insert_pure_sync_user_data = """
    INSERT INTO pure_sync_user_data ps
    (
      ps.person_id,
      ps.first_name,
      ps.last_name,
      ps.user_name,
      ps.email,
      ps.created,
      ps.modified
    )
    SELECT
      pss.person_id,
      pss.first_name,
      pss.last_name,
      pss.user_name,
      pss.email,
      SYSDATE,
      SYSDATE
    FROM pure_sync_user_data_scratch pss
    LEFT OUTER JOIN pure_sync_user_data ps
    ON pss.person_id = ps.person_id
    WHERE ps.person_id IS NULL
    """
record_reporting_of_umn_data_errors = """
    update umn_data_error set reported = sysdate where reported is null
    """

unreported_umn_data_errors = """
    select * from umn_data_error where reported is null
    """

update_pure_sync_person_data = """
    MERGE INTO pure_sync_person_data ps
    USING pure_sync_person_data_scratch pss
    ON (pss.person_id = ps.person_id)
    WHEN MATCHED
      THEN UPDATE SET
        ps.first_name = pss.first_name,
        ps.last_name = pss.last_name,
        ps.postnominal = pss.postnominal,
        ps.emplid = pss.emplid,
        ps.internet_id = pss.internet_id,
        ps.visibility = pss.visibility,
        ps.profiled = pss.profiled,
        ps.modified = SYSDATE
      WHERE
        ORA_HASH(ps.first_name || ps.last_name || ps.postnominal || ps.emplid || ps.internet_id || ps.visibility || ps.profiled)
        <>
        ORA_HASH(pss.first_name || pss.last_name || pss.postnominal || pss.emplid || pss.internet_id || pss.visibility || pss.profiled)
        """

        #-- Can't use the following, because Oracle will attempt to insert nulls if
        #-- there are rows in the target table not matched by the source table.
        #-- If only Oracle supported WHEN NOT MATCHED BY SOURCE.
        #--WHEN NOT MATCHED
        #--  THEN INSERT (
        #--  ) VALUES (
        #--  )

update_pure_sync_staff_org_association = """
    MERGE INTO pure_sync_staff_org_association ps
    USING pure_sync_staff_org_association_scratch pss
    ON (pss.staff_org_association_id = ps.staff_org_association_id)
    WHEN MATCHED
      THEN UPDATE SET
        ps.person_id = pss.person_id,
        ps.period_start_date = pss.period_start_date,
        ps.period_end_date = pss.period_end_date,
        ps.org_id = pss.org_id,
        ps.employment_type = pss.employment_type,
        ps.staff_type = pss.staff_type,
        ps.visibility = pss.visibility,
        ps.primary_association = pss.primary_association,
        ps.job_description = pss.job_description,
        ps.affiliation_id = pss.affiliation_id,
        ps.email_address = pss.email_address,
        ps.modified = SYSDATE
      WHERE
        ORA_HASH(ps.person_id || ps.period_start_date || ps.period_end_date || ps.org_id || ps.employment_type || ps.staff_type || ps.visibility || ps.primary_association || ps.job_description || ps.affiliation_id || ps.email_address)
        <>
        ORA_HASH(pss.person_id || pss.period_start_date || pss.period_end_date || pss.org_id || pss.employment_type || pss.staff_type || pss.visibility || pss.primary_association || pss.job_description || pss.affiliation_id || pss.email_address)
        """
        #-- Can't use the following, because Oracle will attempt to insert nulls if
        #-- there are rows in the target table not matched by the source table.
        #-- If only Oracle supported WHEN NOT MATCHED BY SOURCE.
        #--WHEN NOT MATCHED
        #--  THEN INSERT (
        #--  ) VALUES (
        #--  )

update_pure_sync_student_org_association = """
    MERGE INTO pure_sync_student_org_association ps
    USING pure_sync_student_org_association_scratch pss
    ON (pss.student_org_association_id = ps.student_org_association_id)
    WHEN MATCHED
      THEN UPDATE SET
        ps.person_id = pss.person_id,
        ps.period_start_date = pss.period_start_date,
        ps.period_end_date = pss.period_end_date,
        ps.org_id = pss.org_id,
        ps.status = pss.status,
        ps.affiliation_id = pss.affiliation_id,
        ps.student_type_description = pss.student_type_description,
        ps.email_address = pss.email_address,
        ps.modified = SYSDATE
      WHERE
        ORA_HASH(ps.person_id || ps.period_start_date || ps.period_end_date || ps.org_id || ps.status || ps.affiliation_id || ps.student_type_description || ps.email_address)
        <>
        ORA_HASH(pss.person_id || pss.period_start_date || pss.period_end_date || pss.org_id || pss.status || pss.affiliation_id || pss.student_type_description || pss.email_address)
        """
        #-- Can't use the following, because Oracle will attempt to insert nulls if
        #-- there are rows in the target table not matched by the source table.
        #-- If only Oracle supported WHEN NOT MATCHED BY SOURCE.
        #--WHEN NOT MATCHED
        #--  THEN INSERT (
        #--  ) VALUES (
        #--  )

update_pure_sync_user_data = """
    MERGE INTO pure_sync_user_data ps
    USING pure_sync_user_data_scratch pss
    ON (pss.person_id = ps.person_id)
    WHEN MATCHED
      THEN UPDATE SET
        ps.first_name = pss.first_name,
        ps.last_name = pss.last_name,
        ps.user_name = pss.user_name,
        ps.email = pss.email,
        ps.modified = SYSDATE
      WHERE
        ORA_HASH(ps.first_name || ps.last_name || ps.user_name || ps.email)
        <>
        ORA_HASH(pss.first_name || pss.last_name || pss.user_name || pss.email)
        """

        #-- Can't use the following, because Oracle will attempt to insert nulls if
        #-- there are rows in the target table not matched by the source table.
        #-- If only Oracle supported WHEN NOT MATCHED BY SOURCE.
        #--WHEN NOT MATCHED
        #--  THEN INSERT (
        #--    ps.person_id,
        #--    ps.first_name,
        #--    ps.last_name,
        #--    ps.user_name,
        #--    ps.email,
        #--    ps.created,
        #--    ps.modified
        #--  ) VALUES (
        #--    pss.person_id,
        #--    pss.first_name,
        #--    pss.last_name,
        #--    pss.user_name,
        #--    pss.email,
        #--    SYSDATE,
        #--    SYSDATE
        #--  )
