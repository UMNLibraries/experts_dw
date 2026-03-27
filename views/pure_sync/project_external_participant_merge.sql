MERGE INTO pure_sync_project_external_participant participant
USING (
  SELECT
    project_id,
    emplid,
    first_name,
    last_name,
    role,
    award_id
  FROM pure_sync_project_external_participant_transform_vw
) participant_transform
ON (participant.award_id = participant_transform.award_id AND participant.emplid = participant_transform.emplid AND participant.role = participant_transform.role)
WHEN MATCHED
  THEN UPDATE SET
    participant.project_id = participant_transform.project_id,
    participant.first_name = participant_transform.first_name,
    participant.last_name = participant_transform.last_name,
    participant.updated = SYSDATE
  WHERE (
    participant.project_id <> participant_transform.project_id OR
    participant.first_name <> participant_transform.first_name OR
    participant.last_name <> participant_transform.last_name
  )  
WHEN NOT MATCHED THEN
  INSERT (
    participant.project_id,
    participant.emplid,
    participant.first_name,
    participant.last_name,
    participant.role,
    participant.award_id,
    participant.inserted,
    participant.updated
  )
  VALUES (
    participant_transform.project_id,
    participant_transform.emplid,
    participant_transform.first_name,
    participant_transform.last_name,
    participant_transform.role,
    participant_transform.award_id,
    SYSDATE,
    SYSDATE
  );
