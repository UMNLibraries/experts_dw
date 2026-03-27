-- Column names derived from the Pure project XSD:
-- https://static.helpjuice.com/helpjuice_production/uploads/upload/image/15881/3646974/project.xsd

CREATE OR REPLACE FORCE EDITIONABLE VIEW expert.pure_sync_project_internal_participant_transform_vw (
  project_id,
  person_id,
  emplid, -- Added by UMN
  organisation_id,
  role,
  association_start_date,
  association_end_date,
  award_id -- Added by UMN
) AS (
  SELECT
    project.project_id,
    pure_person.person_id,
    pure_person.emplid,
    pure_staff_org.org_id AS organisation_id,
    LOWER(project_team.proj_role) AS role,
    project_team.start_dt AS association_start_date,
    project_team.end_dt AS association_end_date,
    award.award_id
  FROM pure_sync_project project 
  JOIN pure_sync_award award
    ON project.project_id = award.project_id 
  JOIN fs_ps_project_team_vw@dweprd.oit project_team
    ON award.award_id = project_team.project_id
  JOIN pure_sync_person_data pure_person
    ON pure_person.emplid = project_team.assign_emplid
  JOIN pure_sync_staff_org_association pure_staff_org
    ON pure_person.person_id = pure_staff_org.person_id
  WHERE pure_staff_org.primary_association = 1
);

GRANT SELECT ON expert.pure_sync_project_internal_participant_transform_vw TO oit_expert_rd_all;
