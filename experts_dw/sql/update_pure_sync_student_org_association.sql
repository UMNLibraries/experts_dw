-- :name update_pure_sync_student_org_association :affected
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
    ps.email_address = pss.email_address,
    ps.modified = SYSDATE
  WHERE
    ORA_HASH(ps.person_id || ps.period_start_date || ps.period_end_date || ps.org_id || ps.status || ps.affiliation_id || ps.email_address)
    <>
    ORA_HASH(pss.person_id || pss.period_start_date || pss.period_end_date || pss.org_id || pss.status || pss.affiliation_id || pss.email_address)

-- Can't use the following, because Oracle will attempt to insert nulls if
-- there are rows in the target table not matched by the source table.
-- If only Oracle supported WHEN NOT MATCHED BY SOURCE.
--WHEN NOT MATCHED
--  THEN INSERT (
--  ) VALUES (
--  )
