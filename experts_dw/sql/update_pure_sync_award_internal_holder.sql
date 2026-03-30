-- :name update_pure_sync_award_internal_holder :affected
MERGE INTO pure_sync_award_internal_holder holder
USING (
  SELECT
    award_id,
    person_id,
    emplid,
    organisation_id,
    role,
    association_start_date,
    association_end_date
  FROM pure_sync_award_internal_holder_transform_vw
) holder_transform
ON (holder.award_id = holder_transform.award_id AND holder.person_id = holder_transform.person_id AND holder.role = holder_transform.role)
WHEN MATCHED
  THEN UPDATE SET
    holder.emplid = holder_transform.emplid,
    holder.organisation_id = holder_transform.organisation_id,
    holder.association_start_date = holder_transform.association_start_date,
    holder.association_end_date = holder_transform.association_end_date,
    holder.updated = SYSDATE
  WHERE ORA_HASH(
    holder.emplid ||
    holder.organisation_id ||
    holder.association_start_date ||
    holder.association_end_date
  ) <> ORA_HASH(
    holder_transform.emplid ||
    holder_transform.organisation_id ||
    holder_transform.association_start_date ||
    holder_transform.association_end_date
  )
WHEN NOT MATCHED THEN
  INSERT (
    holder.award_id,
    holder.person_id,
    holder.emplid,
    holder.organisation_id,
    holder.role,
    holder.association_start_date,
    holder.association_end_date,
    holder.inserted,
    holder.updated
  )
  VALUES (
    holder_transform.award_id,
    holder_transform.person_id,
    holder_transform.emplid,
    holder_transform.organisation_id,
    holder_transform.role,
    holder_transform.association_start_date,
    holder_transform.association_end_date,
    SYSDATE,
    SYSDATE
  )
