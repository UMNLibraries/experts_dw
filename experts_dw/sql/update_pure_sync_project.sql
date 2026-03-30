-- :name update_pure_sync_project :affected
MERGE INTO pure_sync_project project
USING (
  SELECT
    project_id,
    title,
    short_title,
    start_date,
    end_date,
    managed_by_organisation_id,
    managed_by_organisation_deptid,
    sponsor_award_number
  FROM pure_sync_project_transform_vw
) project_transform
ON (project.project_id = project_transform.project_id)
WHEN MATCHED
  THEN UPDATE SET
    project.title = project_transform.title,
    project.short_title = project_transform.short_title,
    project.start_date = project_transform.start_date,
    project.end_date = project_transform.end_date,
    project.managed_by_organisation_id = project_transform.managed_by_organisation_id,
    project.managed_by_organisation_deptid = project_transform.managed_by_organisation_deptid,
    project.sponsor_award_number = project_transform.sponsor_award_number,
    project.updated = SYSDATE
  WHERE ORA_HASH(
    project.title ||
    project.short_title ||
    project.start_date ||
    project.end_date ||
    project.managed_by_organisation_id ||
    project.managed_by_organisation_deptid ||
    project.sponsor_award_number
  ) <> ORA_HASH(
    project_transform.title || 
    project_transform.short_title || 
    project_transform.start_date || 
    project_transform.end_date || 
    project_transform.managed_by_organisation_id || 
    project_transform.managed_by_organisation_deptid || 
    project_transform.sponsor_award_number
  )  
WHEN NOT MATCHED THEN
  INSERT (
    project.project_id,
    project.title,
    project.short_title,
    project.start_date,
    project.end_date,
    project.managed_by_organisation_id,
    project.managed_by_organisation_deptid,
    project.sponsor_award_number,
    project.inserted,
    project.updated
  )
  VALUES (
    project_transform.project_id,
    project_transform.title,
    project_transform.short_title,
    project_transform.start_date,
    project_transform.end_date,
    project_transform.managed_by_organisation_id,
    project_transform.managed_by_organisation_deptid,
    project_transform.sponsor_award_number,
    SYSDATE,
    SYSDATE
  )
