-- :name insert_pure_sync_user_data
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
