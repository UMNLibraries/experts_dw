-- Column names derived from the Pure award XSD:
-- https://static.helpjuice.com/helpjuice_production/uploads/upload/image/15881/3646760/award.xsd

CREATE OR REPLACE FORCE EDITIONABLE VIEW expert.pure_sync_award_transform_vw (
  award_id,
  title,
  short_title,
  actual_start_date,
  actual_end_date,
  award_date,
  project_id,
  umn_award_contract_number,
  umn_previous_award_contract_number,
  managed_by_organisation_id,
  managed_by_organisation_deptid, -- Added by UMN
  emplid,
  sponsor_award_number,
  primary_sponsor_award_number,
  federal_award_number,
  financial_funding_id,
  financial_funding_external_org_name,
  financial_funding_primary_id,
  financial_funding_primary_external_org_name
) AS (
  SELECT
    award.contract_num AS award_id, -- award:upmaward id="{{ project.project_id }}"
    --'other/award' as "type", -- award:upmaward type="other/award"
    --research -- award:activityTypes > award:activityTypes research
    CASE -- award:title > common:test lang="en" country="US"
      WHEN REGEXP_LIKE(award.descr254, '[[:alnum:]]')
        THEN award.descr254
      WHEN REGEXP_LIKE(award.title56, '[[:alnum:]]')
        THEN award.title56
      ELSE 'Title missing' -- Pure award.xsd requires a title
    END AS title,
    award.title56 as short_title,
    award.begin_dt AS actual_start_date, -- award:actualStartDate {{ award.begin_dt }}
    award.end_dt AS actual_end_date, -- award:actualEndDate {{ award.end_dt }}
    award.begin_dt AS award_date, -- award:awardDate {{ award.begin_dt }}
    -- award:ids >

    award.contract_num AS project_id, -- Do we actually use project_id in the XML? It's in the recommended Oracle view.
    award.contract_num AS umn_award_contract_number, -- common:id type="umn_award_contract_number" {{ award.contract_num }}
    CASE
      WHEN REGEXP_LIKE(award.prev_contract_num, '[[:alnum:]]')
        THEN award.prev_contract_num  -- common:id type="umn_previous_award_contract_number"
      ELSE NULL
    END AS umn_previous_award_contract_number,

    udpo.pure_org_id AS managed_by_organisation_id, -- award:managedByOrganisation id="{{ udpo.pure_org_id }}"
    udpo.deptid AS managed_by_organisation_deptid,
    award.emplid,
    CASE
      WHEN REGEXP_LIKE(award.ref_awd_number, '[[:alnum:]]')
        THEN award.ref_awd_number  -- common:id type="sponsor_award_number" {{ award.ref_awd_number }}
      ELSE NULL
    END AS sponsor_award_number,
    CASE
      WHEN REGEXP_LIKE(award.ref_awd_num2, '[[:alnum:]]') AND award.ref_awd_num2 <> award.ref_awd_number
        THEN award.ref_awd_num2  -- common:id type="primary_sponsor_award_number" {{ award.ref_awd_num2 }}
      ELSE NULL
    END AS primary_sponsor_award_number,
    CASE
      WHEN REGEXP_LIKE(award.fed_awd_id_number, '[[:alnum:]]')
        THEN award.fed_awd_id_number  -- common:id type="federal_award_number" {{ award.fed_awd_id_number }}
      ELSE NULL
    END AS federal_award_number,
    -- award:financialFundings >
    CASE
      WHEN REGEXP_LIKE(award.cust_id, '[[:alnum:]]')
	THEN award.cust_id
      ELSE NULL
    END AS financial_funding_id, -- award:financialFudning id="{{ award.cust_id }}" >
    CASE
      WHEN REGEXP_LIKE(award.cust_id, '[[:alnum:]]')
	THEN customer.name1
      ELSE NULL -- No point in setting an org name if the id is NULL or otherwise worthless.
    END AS financial_funding_external_org_name, -- award:externalOrgName {{ customer.name1 }}
    -- 'sponsor', -- award:externalOrgType sponsor
    CASE
      WHEN REGEXP_LIKE(award.primary_spnsr_id, '[[:alnum:]]') AND award.primary_spnsr_id <> award.cust_id
	THEN award.primary_spnsr_id
      ELSE NULL
    END AS financial_funding_primary_id,
    CASE
      WHEN REGEXP_LIKE(award.primary_spnsr_id, '[[:alnum:]]') AND award.primary_spnsr_id <> award.cust_id
      THEN -- award:financialFunding id="{{ award.primary_spnsr_id }}" >
          customer2.name1 -- award:externalOrgName {{ customer2.name1 }}
          -- 'primary_sponsor' -- award:externalOrgType primary_sponsor
      ELSE NULL  -- No point in setting an org name if the id is NULL or otherwise worthless.
    END AS financial_funding_primary_external_org_name
    -- 'Public' -- award:visibility Public
  FROM fs_ps_gm_award@dweprd.oit award
  JOIN pure_sync_project project
    -- Ensure that the award.project_id FK on project.project_id will not break:
    ON award.contract_num = project.project_id
  JOIN umn_dept_pure_org udpo
    ON udpo.deptid = award.deptid
  JOIN fs_ps_customer@dweprd.oit customer
    ON customer.cust_id = award.cust_id
  LEFT JOIN fs_ps_customer@dweprd.oit customer2
    ON customer2.cust_id = award.primary_spnsr_id
  WHERE award.award_status NOT IN ('TER','TRA','WTH') --Include only legitimate awards.
);

GRANT SELECT ON expert.pure_sync_award_transform_vw TO oit_expert_rd_all;
