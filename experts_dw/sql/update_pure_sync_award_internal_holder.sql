-- :name update_pure_sync_award_internal_holder :affected
MERGE INTO pure_sync_award_internal_holder holder
USING (
  SELECT
    award_id,
    person_id,
    emplid,
    organisation_id,
    role
  FROM pure_sync_award_internal_holder_transform_vw
  WHERE award_person_row_number = 1
) holder_transform
ON (holder.award_id = holder_transform.award_id AND holder.person_id = holder_transform.person_id)
WHEN MATCHED
  THEN UPDATE SET
    holder.emplid = holder_transform.emplid,
    holder.organisation_id = holder_transform.organisation_id,
    holder.role = holder_transform.role,
    holder.updated = SYSDATE
  WHERE ORA_HASH(
    holder.emplid ||
    holder.organisation_id ||
    holder.role
  ) <> ORA_HASH(
    holder_transform.emplid ||
    holder_transform.organisation_id ||
    holder_transform.role
  )
WHEN NOT MATCHED THEN
  INSERT (
    holder.award_id,
    holder.person_id,
    holder.emplid,
    holder.organisation_id,
    holder.role,
    holder.inserted,
    holder.updated
  )
  VALUES (
    holder_transform.award_id,
    holder_transform.person_id,
    holder_transform.emplid,
    holder_transform.organisation_id,
    holder_transform.role,
    SYSDATE,
    SYSDATE
  )
