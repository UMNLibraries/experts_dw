-- :name insert_pure_sync_student_org_association
INSERT INTO pure_sync_student_org_association ps
(
  ps.student_org_association_id,
  ps.person_id,
  ps.period_start_date,
  ps.period_end_date,
  ps.org_id,
  ps.status,
  ps.affiliation_id,
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
  pss.email_address,
  SYSDATE,
  SYSDATE
FROM pure_sync_student_org_association_scratch pss
LEFT OUTER JOIN pure_sync_student_org_association ps
ON pss.student_org_association_id = ps.student_org_association_id
WHERE ps.student_org_association_id IS NULL
