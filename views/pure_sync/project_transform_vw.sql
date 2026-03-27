-- Column names derived from the Pure project XSD:
-- https://static.helpjuice.com/helpjuice_production/uploads/upload/image/15881/3646974/project.xsd

CREATE OR REPLACE FORCE EDITIONABLE VIEW expert.pure_sync_project_transform_vw (
  project_id,
  title,
  short_title,
  --description, -- Replacing this with short_title, to make it consistent with awards.
  start_date,
  end_date,
  managed_by_organisation_id,
  managed_by_organisation_deptid, -- Added by UMN
  sponsor_award_number -- Added by UMN
) AS (
  SELECT
    award.contract_num AS project_id, -- project:upmproject id="{{ award.contract_num }}" type="research"
    -- Replacing the strange handling of titles and descriptions below with the more
    -- straight-forward code we use for awards.
    /*
    CASE -- project:title > common:text lang="en" country="US"
      WHEN REGEXP_LIKE(award.descr254, '[[:alnum:]]')
        THEN REGEXP_REPLACE(REGEXP_REPLACE(award.descr254, '^\"',''), '\"$','')
      ELSE REGEXP_REPLACE(REGEXP_REPLACE(award.title56, '^\"',''), '\"$','')
    END AS title,
    REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_REPLACE(award.descr254, '\s',' '), '^\"',''), '\"$','') AS description, -- project:descriptions > common:description type="projectdescription" > common:text lang="en" country="US" {{ award.descr254 }}
    */
    CASE
      WHEN REGEXP_LIKE(award.descr254, '[[:alnum:]]')
        THEN award.descr254
      WHEN REGEXP_LIKE(award.title56, '[[:alnum:]]')
        THEN award.title56
      ELSE 'Title missing' -- Pure upmproject.xsd requires a title
    END AS title,
    award.title56 as short_title,
    award.begin_dt AS start_date, -- project:startDate {{ award.begin_dt }}
    award.end_dt AS end_date, -- project:endDate {{ award.end_dt }}
    udpo.pure_org_id AS managed_by_organisaiton_id, -- project:managedByOrganisation id="{{ udpo.pure_org_id }}"
    award.deptid AS managed_by_organisation_deptid,
    -- Decided not to duplicate the contract_num/um_award_number. We'll use project_id instead.
    --award.contract_num AS um_award_number, -- common:id type="um_award_number" {{ award.contract_num }}
    CASE
      WHEN REGEXP_LIKE(award.ref_awd_number, '[[:alnum:]]')
        THEN award.ref_awd_number  -- common:id type="sponsor_award_number" {{ award.ref_awd_number }}
      ELSE NULL
    END AS sponsor_award_number -- common:id type="sponsor_award_number" {{ award.ref_awd_number }}
  FROM fs_ps_gm_award@dweprd.oit award
  JOIN umn_dept_pure_org udpo
    ON udpo.deptid = award.deptid
  WHERE award.award_status NOT IN ('TER','TRA','WTH')
);

GRANT SELECT ON expert.pure_sync_project_transform_vw TO oit_expert_rd_all;
