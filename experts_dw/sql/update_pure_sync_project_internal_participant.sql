-- :name update_pure_sync_project_internal_participant :affected
MERGE INTO pure_sync_project_internal_participant participant
USING (
  SELECT
    project_id,
    person_id,
    emplid,
    organisation_id,
    role
  FROM pure_sync_project_internal_participant_transform_vw
  WHERE project_person_row_number = 1
) participant_transform
ON (participant.project_id = participant_transform.project_id AND participant.person_id = participant_transform.person_id)
WHEN MATCHED
  THEN UPDATE SET
    participant.emplid = participant_transform.emplid,
    participant.organisation_id = participant_transform.organisation_id,
    participant.role = participant_transform.role,
    participant.updated = SYSDATE
  WHERE ORA_HASH(
    participant.emplid ||
    participant.organisation_id ||
    participant.role
  ) <> ORA_HASH(
    participant_transform.emplid ||
    participant_transform.organisation_id ||
    participant_transform.role
  )
WHEN NOT MATCHED THEN
  INSERT (
    participant.project_id,
    participant.person_id,
    participant.emplid,
    participant.organisation_id,
    participant.role,
    participant.inserted,
    participant.updated
  )
  VALUES (
    participant_transform.project_id,
    participant_transform.person_id,
    participant_transform.emplid,
    participant_transform.organisation_id,
    participant_transform.role,
    SYSDATE,
    SYSDATE
  )
