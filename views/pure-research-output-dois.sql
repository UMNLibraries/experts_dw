-- View converting publication externalIds to columns indexed by UUID
-- Use for joining to other queries and getting a flat view of other identifiers

-- DEPEDNDS ON:
-- no views

-- DEPENDENTS VIEWS:
-- pure_research_output_pub
DROP MATERIALIZED VIEW jsonview_pure_research_output_doi; COMMIT; 
CREATE MATERIALIZED VIEW jsonview_pure_research_output_doi
  BUILD DEFERRED
  REFRESH ON DEMAND
AS
SELECT
  uuid,
  doi_openaccess,
  COALESCE(doi_restricted, doi_unknown) AS doi
FROM (
  SELECT
    pi.uuid,
    jval.doi_value,
    -- Not using the type, instead collapsing to open access or not.
    -- COALESCE(REVERSE(REGEXP_SUBSTR(REVERSE(jval.doi_type), '[^/]+', 1, 1)), 'unspecified') AS doi_type,
    REVERSE(REGEXP_SUBSTR(REVERSE(jval.doi_openaccess_permission), '[^/]+', 1, 1)) AS doi_openaccess_permission
  FROM
    PURE_JSON_RESEARCH_OUTPUT_516 pi,
    JSON_TABLE(pi.JSON_DOCUMENT, '$'
      COLUMNS (
        NESTED PATH '$.electronicVersions[*]'
          COLUMNS (
            doi_value VARCHAR2(255) PATH '$.doi',
            -- Not using the type, instead collapsing to open access or not.
            -- doi_type VARCHAR2(150) PATH '$.versionType.uri',
            doi_openaccess_permission VARCHAR2(150) PATH '$.accessType.uri'
          )
      )) jval
  )
  PIVOT (
    MAX(doi_value)
    FOR doi_openaccess_permission IN ('open' AS doi_openaccess, 'restricted' AS doi_restricted, 'unknown' AS doi_unknown)
  )
;
CREATE INDEX idx_pure_research_output_doi_uuid ON jsonview_pure_research_output_doi (uuid);
CREATE INDEX idx_pure_research_output_doi_doi ON jsonview_pure_research_output_doi (doi);
EXECUTE DBMS_MVIEW.REFRESH('jsonview_pure_research_output_doi');
