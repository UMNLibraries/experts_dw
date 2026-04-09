-- :name update_pure_sync_award_external_holder :affected
MERGE INTO pure_sync_award_external_holder holder
USING (
  SELECT
    award_id,
    emplid,
    first_name,
    last_name,
    role
  FROM pure_sync_award_external_holder_transform_vw
  WHERE award_person_row_number = 1
) holder_transform
ON (holder.award_id = holder_transform.award_id AND holder.emplid = holder_transform.emplid)
WHEN MATCHED
  THEN UPDATE SET
    holder.first_name = holder_transform.first_name,
    holder.last_name = holder_transform.last_name,
    holder.role = holder_transform.role,
    holder.updated = SYSDATE
  WHERE ORA_HASH(
    holder.first_name ||
    holder.last_name ||
    holder.role
  ) <> ORA_HASH(
    holder_transform.first_name ||
    holder_transform.last_name ||
    holder_transform.role
  )
WHEN NOT MATCHED THEN
  INSERT (
    holder.award_id,
    holder.emplid,
    holder.first_name,
    holder.last_name,
    holder.role,
    holder.inserted,
    holder.updated
  )
  VALUES (
    holder_transform.award_id,
    holder_transform.emplid,
    holder_transform.first_name,
    holder_transform.last_name,
    holder_transform.role,
    SYSDATE,
    SYSDATE
  )
