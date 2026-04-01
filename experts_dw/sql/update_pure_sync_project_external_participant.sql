-- :name update_pure_sync_project_external_participant :affected
MERGE INTO pure_sync_project_external_participant participant
USING (
  SELECT
    project_id,
    emplid,
    first_name,
    last_name,
    role
  FROM pure_sync_project_external_participant_transform_vw
  WHERE project_person_row_number = 1
) participant_transform
ON (participant.project_id = participant_transform.project_id AND participant.emplid = participant_transform.emplid)
WHEN MATCHED
  THEN UPDATE SET
    participant.first_name = participant_transform.first_name,
    participant.last_name = participant_transform.last_name,
    participant.role = participant_transform.role,    
    participant.updated = SYSDATE
  WHERE ORA_HASH(
    participant.first_name ||
    participant.last_name ||
    participant.role
  ) <> ORA_HASH(
    participant_transform.first_name ||
    participant_transform.last_name ||
    participant_transform.role
  )
WHEN NOT MATCHED THEN
  INSERT (
    participant.project_id,
    participant.emplid,
    participant.first_name,
    participant.last_name,
    participant.role,
    participant.inserted,
    participant.updated
  )
  VALUES (
    participant_transform.project_id,
    participant_transform.emplid,
    participant_transform.first_name,
    participant_transform.last_name,
    participant_transform.role,
    SYSDATE,
    SYSDATE
  )
