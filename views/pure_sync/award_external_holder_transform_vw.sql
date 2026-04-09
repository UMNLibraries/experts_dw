-- Column names derived from the Pure award XSD:
-- https://static.helpjuice.com/helpjuice_production/uploads/upload/image/15881/3646760/award.xsd

CREATE OR REPLACE FORCE EDITIONABLE VIEW expert.pure_sync_award_external_holder_transform_vw (
  award_id,
  emplid, -- Added by UMN
  first_name,
  last_name,
  role,
  role_rank, -- Added by UMN

  -- Though we don't use these in the final XML output,
  -- we include them here anyway, for debugging/troubleshooting.
  association_start_date,
  association_end_date,

  umn_project_id, -- Added by UMN
  award_person_row_number -- Added by UMN
) AS (
  SELECT
    award_person.*,
    ROW_NUMBER() OVER (
      -- This partitions by both columns, first award_id, then emplid:
      PARTITION BY award_person.award_id, award_person.emplid
      -- Ordering rows by role_rank within each partition ensures that the
      -- highest-ranking role will always be in the first row for each person:
      ORDER BY award_person.role_rank ASC
    ) AS award_person_row_number
  FROM (
    SELECT
      award.award_id,
      hr_demog.emplid,
      hr_demog.first_name,
      hr_demog.last_name,
      LOWER(project_team.proj_role) AS role,
      CASE
        WHEN project_team.proj_role = 'PI' THEN 1
        WHEN project_team.proj_role = 'COI' THEN 2
        WHEN project_team.proj_role = 'CPI' THEN 3
        WHEN project_team.proj_role = 'PROJECT_MANAGER' THEN 4
        WHEN project_team.proj_role = 'KEY' THEN 5
        WHEN project_team.proj_role = 'CONS' THEN 6
        WHEN project_team.proj_role = 'GRAD' THEN 7
        WHEN project_team.proj_role = 'PPI' THEN 8
        WHEN project_team.proj_role = 'OTH' THEN 9
        WHEN project_team.proj_role = 'OTHR' THEN 10
        ELSE 10
      END AS role_rank,
      project_team.start_dt AS association_start_date,
      project_team.end_dt AS association_end_date,
      project_team.project_id AS umn_project_id
    FROM pure_sync_award award
    JOIN fs_ps_gm_awd_projt_vw@dweprd.oit award_project
      -- We use the UMN award contract number for Pure award IDs:
      ON award.award_id = award_project.contract_num
    JOIN fs_ps_project_team_vw@dweprd.oit project_team
      ON award_project.project_id = project_team.project_id
      -- For Pure award records, include only the person on the UMN award record:
      AND award.emplid = project_team.assign_emplid
    JOIN ps_dwhr_demo_addr_vw@dweprd.oit hr_demog
      ON hr_demog.emplid = project_team.assign_emplid
    LEFT JOIN pure_sync_person_data pure_person
      ON project_team.assign_emplid = pure_person.emplid
    WHERE pure_person.emplid IS NULL
  ) award_person
);

GRANT SELECT ON expert.pure_sync_award_external_holder_transform_vw TO oit_expert_rd_all;
