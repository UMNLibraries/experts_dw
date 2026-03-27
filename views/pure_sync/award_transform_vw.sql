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
  managed_by_organisation_id,
  managed_by_organisation_deptid, -- Added by UMN
  sponsor_award_number,
  primary_sponsor_award_number,
  financial_funding_id,
  financial_funding_external_org_name,
  financial_funding_primary_id,
  financial_funding_primary_external_org_name
) AS (
  SELECT
    award_project.project_id AS award_id, -- award:upmaward id="{{ project.project_id }}"
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
    CASE
      WHEN award.award_dt IS NOT NULL
	THEN award.award_dt
      WHEN award.begin_dt IS NOT NULL
	THEN award.begin_dt
      ELSE TO_DATE('1970-01-01','YYYY-MM-DD') -- Pure award.xsd requires an awardDate
    END AS award_date, -- award:awardDate {{ award.begin_dt }}
    -- award:ids >
    award.contract_num AS project_id, -- Do we actually use project_id in the XML? It's in the recommended Oracle view.
    -- Decided not to duplicate the contract_num/um_award_number. We'll use project_id instead.
    --award.contract_num AS um_award_number, -- common:id type="um_award_number" {{ award.contract_num }}
    udpo.pure_org_id AS managed_by_organisation_id, -- award:managedByOrganisation id="{{ udpo.pure_org_id }}"
    udpo.deptid AS managed_by_organisation_deptid,
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
  JOIN umn_dept_pure_org udpo
    ON udpo.deptid = award.deptid
  JOIN fs_ps_gm_awd_projt_vw@dweprd award_project
    ON award_project.contract_num = award.contract_num
  JOIN pure_sync_project project
    ON award.contract_num = project.project_id
  JOIN fs_ps_customer@dweprd.oit customer
    ON customer.cust_id = award.cust_id
  LEFT JOIN fs_ps_customer@dweprd.oit customer2
    ON customer2.cust_id = award.primary_spnsr_id
  WHERE award.award_status NOT IN ('TER','TRA','WTH') --Include only legitimate awards.
);

GRANT SELECT ON expert.pure_sync_award_transform_vw TO oit_expert_rd_all;
