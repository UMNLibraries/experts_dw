-- :name update_pure_sync_user_data :affected
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
    ORA_HASH(pss.first_name || pss.last_name || pss.user_name || pss.email);

-- Can't use the following, because Oracle will attempt to insert nulls if
-- there are rows in the target table not matched by the source table.
-- If only Oracle supported WHEN NOT MATCHED BY SOURCE.
--WHEN NOT MATCHED
--  THEN INSERT (
--    ps.person_id,
--    ps.first_name,
--    ps.last_name,
--    ps.user_name,
--    ps.email,
--    ps.created,
--    ps.modified
--  ) VALUES (
--    pss.person_id,
--    pss.first_name,
--    pss.last_name,
--    pss.user_name,
--    pss.email,
--    SYSDATE,
--    SYSDATE
--  );
