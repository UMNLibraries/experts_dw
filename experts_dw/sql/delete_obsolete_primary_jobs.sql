-- :name delete_obsolete_primary_jobs
DELETE FROM pure_sync_staff_org_association ps
WHERE ps.primary_association = 1
AND ps.modified < (
  SELECT MAX(ps2.modified)
  FROM pure_sync_staff_org_association ps2
  WHERE ps2.primary_association = 1
  AND ps2.person_id = ps.person_id
)
