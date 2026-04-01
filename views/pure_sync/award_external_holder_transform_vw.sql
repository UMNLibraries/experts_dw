-- Column names derived from the Pure award XSD:
-- https://static.helpjuice.com/helpjuice_production/uploads/upload/image/15881/3646760/award.xsd

CREATE OR REPLACE FORCE EDITIONABLE VIEW expert.pure_sync_award_external_holder_transform_vw (
  award_id,
  emplid, -- Added by UMN
  first_name,
  last_name,
  role,
  association_start_date,
  association_end_date
) AS (
  SELECT
    project_team.project_id AS award_id,
    hr_demog.emplid,
    hr_demog.first_name,
    hr_demog.last_name,
    LOWER(project_team.proj_role) AS role,
    project_team.start_dt AS association_start_date,
    project_team.end_dt AS association_end_date
  FROM pure_sync_award award
  JOIN fs_ps_project_team_vw@dweprd.oit project_team
    ON award.award_id = project_team.project_id
  JOIN ps_dwhr_demo_addr_vw@dweprd.oit hr_demog
    ON hr_demog.emplid = project_team.assign_emplid
  LEFT JOIN pure_sync_person_data pure_person
    ON project_team.assign_emplid = pure_person.emplid
  WHERE pure_person.emplid IS NULL
);

GRANT SELECT ON expert.pure_sync_award_external_holder_transform_vw TO oit_expert_rd_all;
