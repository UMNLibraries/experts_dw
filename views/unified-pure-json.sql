-- DEPENDS ON:
-- no views, all pure_json_* tables

-- REFRESH TIME (tst): 1170s
-- REFRESH TIME (prd): 1305s
-- RUN ORDER: 1

DROP MATERIALIZED VIEW jsonview_unified_pure_json;
CREATE MATERIALIZED VIEW jsonview_unified_pure_json
  BUILD DEFERRED
  REFRESH ON DEMAND
AS
SELECT uuid, pure_modified, 'pure_json_research_output' AS source, json_document FROM pure_json_research_output_517
UNION ALL
SELECT uuid, pure_modified, 'pure_json_person' AS source, json_document FROM pure_json_person_517
UNION ALL
SELECT uuid, pure_modified, 'pure_json_external_person' AS source, json_document FROM pure_json_external_person_517
UNION ALL
SELECT uuid, pure_modified, 'pure_json_organisation' AS source, json_document FROM pure_json_organisation_517
UNION ALL
SELECT uuid, pure_modified, 'pure_json_external_organisation' AS source, json_document FROM pure_json_external_organisation_517
;
CREATE INDEX idx_jsonview_unified_pure_json_uuid ON jsonview_unified_pure_json (uuid);
CREATE INDEX idx_jsonview_unified_pure_json_source ON jsonview_unified_pure_json (source);
EXECUTE DBMS_MVIEW.REFRESH('jsonview_unified_pure_json');
