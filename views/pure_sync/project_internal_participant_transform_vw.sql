-- Column names derived from the Pure project XSD:
-- https://static.helpjuice.com/helpjuice_production/uploads/upload/image/15881/3646974/project.xsd

CREATE OR REPLACE FORCE EDITIONABLE VIEW expert.pure_sync_project_internal_participant_transform_vw (
  project_id,
  person_id,
  emplid, -- Added by UMN
  organisation_id,
  role,
  role_rank, -- Added by UMN

  -- Though we don't use these in the final XML output,
  -- we include them here anyway, for debugging/troubleshooting.
  
  association_start_date,
  association_end_date,

  umn_project_id, -- Added by UMN
  project_person_row_number -- Added by UMN
) AS (
  SELECT
    project_person.*,
    ROW_NUMBER() OVER (
      -- This partitions by both columns, first project_id, then person_id:
      PARTITION BY project_person.project_id, project_person.person_id
      -- Ordering rows by role_rank within each partition ensures that the
      -- highest-ranking role will always be in the first row for each person:
      ORDER BY project_person.role_rank ASC
    ) AS project_person_row_number
  FROM (
    SELECT
      project.project_id,
      pure_person.person_id,
      pure_person.emplid,
      pure_staff_org.org_id AS organisation_id,
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
    FROM pure_sync_project project
    JOIN fs_ps_gm_awd_projt_vw@dweprd.oit award_project
      -- We use the UMN award contract number for Pure project IDs:
      ON project.project_id = award_project.contract_num
    JOIN fs_ps_project_team_vw@dweprd.oit project_team
      ON award_project.project_id = project_team.project_id
    JOIN pure_sync_person_data pure_person
      ON pure_person.emplid = project_team.assign_emplid
    JOIN pure_sync_staff_org_association pure_staff_org
      ON pure_person.person_id = pure_staff_org.person_id
    WHERE pure_staff_org.primary_association = 1
  ) project_person
);

GRANT SELECT ON expert.pure_sync_project_internal_participant_transform_vw TO oit_expert_rd_all;
