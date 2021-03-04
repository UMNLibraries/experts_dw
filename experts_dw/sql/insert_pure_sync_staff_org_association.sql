-- :name insert_pure_sync_staff_org_association
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
