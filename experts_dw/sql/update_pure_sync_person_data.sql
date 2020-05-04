-- :name update_pure_sync_person_data :affected
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
    ORA_HASH(pss.first_name || pss.last_name || pss.postnominal || pss.emplid || pss.internet_id || pss.visibility || pss.profiled);

-- Can't use the following, because Oracle will attempt to insert nulls if
-- there are rows in the target table not matched by the source table.
-- If only Oracle supported WHEN NOT MATCHED BY SOURCE.
--WHEN NOT MATCHED
--  THEN INSERT (
--  ) VALUES (
--  );
