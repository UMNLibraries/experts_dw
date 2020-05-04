-- :name insert_pure_sync_person_data :insert
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
lEFT OUTER JOIN pure_sync_person_data ps
ON pss.person_id = ps.person_id
WHERE ps.person_id IS NULL;
