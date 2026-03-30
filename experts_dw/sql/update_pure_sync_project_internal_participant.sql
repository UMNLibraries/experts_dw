-- :name update_pure_sync_project_internal_participant :affected
MERGE INTO pure_sync_project_internal_participant participant
USING (
  SELECT
    project_id,
    person_id,
    emplid,
    organisation_id,
    role,
    association_start_date,
    association_end_date,
    award_id
  FROM pure_sync_project_internal_participant_transform_vw
) participant_transform
ON (participant.award_id = participant_transform.award_id AND participant.person_id = participant_transform.person_id AND participant.role = participant_transform.role)
WHEN MATCHED
  THEN UPDATE SET
    participant.project_id = participant_transform.project_id,
    participant.emplid = participant_transform.emplid,
    participant.organisation_id = participant_transform.organisation_id,
    participant.association_start_date = participant_transform.association_start_date,
    participant.association_end_date = participant_transform.association_end_date,
    participant.updated = SYSDATE
  WHERE ORA_HASH(
    participant.project_id ||
    participant.emplid ||
    participant.organisation_id ||
    participant.association_start_date ||
    participant.association_end_date
  ) <> ORA_HASH(
    participant_transform.project_id ||
    participant_transform.emplid ||
    participant_transform.organisation_id ||
    participant_transform.association_start_date ||
    participant_transform.association_end_date
  )
WHEN NOT MATCHED THEN
  INSERT (
    participant.project_id,
    participant.person_id,
    participant.emplid,
    participant.organisation_id,
    participant.role,
    participant.association_start_date,
    participant.association_end_date,
    participant.award_id,
    participant.inserted,
    participant.updated
  )
  VALUES (
    participant_transform.project_id,
    participant_transform.person_id,
    participant_transform.emplid,
    participant_transform.organisation_id,
    participant_transform.role,
    participant_transform.association_start_date,
    participant_transform.association_end_date,
    participant_transform.award_id,
    SYSDATE,
    SYSDATE
  )
