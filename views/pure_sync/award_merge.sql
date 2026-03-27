MERGE INTO pure_sync_award award
USING (
  SELECT
    award_id,
    title,
    short_title,
    actual_start_date,
    actual_end_date,
    award_date,
    project_id,
    managed_by_organisation_id,
    managed_by_organisation_deptid,
    sponsor_award_number,
    primary_sponsor_award_number,
    financial_funding_id,
    financial_funding_external_org_name,
    financial_funding_primary_id,
    financial_funding_primary_external_org_name
  FROM pure_sync_award_transform_vw
) award_transform
ON (award.award_id = award_transform.award_id)
WHEN MATCHED
  THEN UPDATE SET
    award.title = award_transform.title,
    award.short_title = award_transform.short_title,
    award.actual_start_date = award_transform.actual_start_date,
    award.actual_end_date = award_transform.actual_end_date,
    award.award_date = award_transform.award_date,
    award.project_id = award_transform.project_id,
    award.managed_by_organisation_id = award_transform.managed_by_organisation_id,
    award.managed_by_organisation_deptid = award_transform.managed_by_organisation_deptid,
    award.sponsor_award_number = award_transform.sponsor_award_number,
    award.primary_sponsor_award_number = award_transform.primary_sponsor_award_number,
    award.financial_funding_id = award_transform.financial_funding_id,
    award.financial_funding_external_org_name = award_transform.financial_funding_external_org_name,
    award.financial_funding_primary_id = award_transform.financial_funding_primary_id,
    award.financial_funding_primary_external_org_name = award_transform.financial_funding_primary_external_org_name,
    award.updated = SYSDATE
  WHERE (
    award.title <> award_transform.title OR 
    award.short_title <> award_transform.short_title OR 
    award.actual_start_date <> award_transform.actual_start_date OR 
    award.actual_end_date <> award_transform.actual_end_date OR 
    award.award_date <> award_transform.award_date OR 
    award.project_id <> award_transform.project_id OR 
    award.managed_by_organisation_id <> award_transform.managed_by_organisation_id OR 
    award.managed_by_organisation_deptid <> award_transform.managed_by_organisation_deptid OR 
    award.sponsor_award_number <> award_transform.sponsor_award_number OR 
    award.primary_sponsor_award_number <> award_transform.primary_sponsor_award_number OR 
    award.financial_funding_id <> award_transform.financial_funding_id OR 
    award.financial_funding_external_org_name <> award_transform.financial_funding_external_org_name OR 
    award.financial_funding_primary_id <> award_transform.financial_funding_primary_id OR 
    award.financial_funding_primary_external_org_name <> award_transform.financial_funding_primary_external_org_name
  )  
WHEN NOT MATCHED THEN
  INSERT (
    award.award_id,
    award.title,
    award.short_title,
    award.actual_start_date,
    award.actual_end_date,
    award.award_date,
    award.project_id,
    award.managed_by_organisation_id,
    award.managed_by_organisation_deptid,
    award.sponsor_award_number,
    award.primary_sponsor_award_number,
    award.financial_funding_id,
    award.financial_funding_external_org_name,
    award.financial_funding_primary_id,
    award.financial_funding_primary_external_org_name,
    award.inserted,
    award.updated
  )
  VALUES (
    award_transform.award_id,
    award_transform.title,
    award_transform.short_title,
    award_transform.actual_start_date,
    award_transform.actual_end_date,
    award_transform.award_date,
    award_transform.project_id,
    award_transform.managed_by_organisation_id,
    award_transform.managed_by_organisation_deptid,
    award_transform.sponsor_award_number,
    award_transform.primary_sponsor_award_number,
    award_transform.financial_funding_id,
    award_transform.financial_funding_external_org_name,
    award_transform.financial_funding_primary_id,
    award_transform.financial_funding_primary_external_org_name,
    SYSDATE,
    SYSDATE
  );
