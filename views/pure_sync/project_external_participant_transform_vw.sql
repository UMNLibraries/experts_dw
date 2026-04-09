-- Column names derived from the Pure project XSD:
-- https://static.helpjuice.com/helpjuice_production/uploads/upload/image/15881/3646974/project.xsd

CREATE OR REPLACE FORCE EDITIONABLE VIEW expert.pure_sync_project_external_participant_transform_vw (
  project_id,
  emplid, -- Added by UMN
  first_name,
  last_name,
  role,
  role_rank, -- Added by UMN

  -- Though these are not part of the XSD referred to above,
  -- we include them here anyway, for debugging/troubleshooting.
  association_start_date, 
  association_end_date,

  umn_project_id, -- Added by UMN
  project_person_row_number -- Added by UMN
) AS (
  SELECT
    project_person.*,
    ROW_NUMBER() OVER (
      -- This partitions by both columns, first project_id, then emplid:
      PARTITION BY project_person.project_id, project_person.emplid
      -- Ordering rows by role_rank within each partition ensures that the
      -- highest-ranking role will always be in the first row for each person:
      ORDER BY project_person.role_rank ASC
    ) AS project_person_row_number
  FROM (
    SELECT
      project.project_id,
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
      project_team.project_id As umn_project_id
    FROM pure_sync_project project
    JOIN fs_ps_gm_awd_projt_vw@dweprd.oit award_project
      -- We use the UMN award contract number for Pure project IDs:
      ON project.project_id = award_project.contract_num
    JOIN fs_ps_project_team_vw@dweprd.oit project_team
      ON award_project.project_id = project_team.project_id
    JOIN ps_dwhr_demo_addr_vw@dweprd.oit hr_demog
      ON hr_demog.emplid = project_team.assign_emplid
    LEFT JOIN pure_sync_person_data pure_person
      ON project_team.assign_emplid = pure_person.emplid
    WHERE pure_person.emplid IS NULL
  ) project_person
);

GRANT SELECT ON expert.pure_sync_project_external_participant_transform_vw TO oit_expert_rd_all;
