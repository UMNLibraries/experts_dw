-- DEPENDS ON:
-- -- unified_pure_json

-- DEPENDENTS:
-- no views

DROP MATERIALIZED VIEW jsonview_person_pure_org; COMMIT;
CREATE MATERIALIZED VIEW jsonview_person_pure_org
  BUILD DEFERRED
  REFRESH ON DEMAND
AS
SELECT
  uuid AS person_uuid,
  -- internal persons use the JSON path from staffOrganisationAssociations
  -- external persons use the path from externalOrganisations but output only one column
  CASE WHEN p.source = 'pure_json_person' THEN org_uuid_internal ELSE org_uuid_external END AS pure_org_uuid
FROM
  jsonview_unified_pure_json p,
  JSON_TABLE(p.JSON_DOCUMENT, '$'
    COLUMNS(
      NESTED PATH '$.staffOrganisationAssociations[*]'
        COLUMNS(
          org_uuid_internal PATH '$.uuid'
        ),
      NESTED PATH '$.externalOrganisations[*]'
        COLUMNS(
          org_uuid_external PATH '$.uuid'
        )
    )) jt
WHERE p.source IN ('pure_json_person', 'pure_json_external_person');

CREATE INDEX idx_jsonview_person_pure_org_person_uuid_org_uuid ON jsonview_person_pure_org (person_uuid, pure_org_uuid);
EXECUTE DBMS_MVIEW.REFRESH('jsonview_person_pure_org');
