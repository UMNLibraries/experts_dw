-- View converting publication externalIds to columns indexed by UUID
-- Use for joining to other queries and getting a flat view of other identifiers

-- DEPEDNDS ON:
-- no views

-- DEPENDENTS VIEWS:
-- pure_research_output_pub
DROP MATERIALIZED VIEW jsonview_pure_research_output_external_ids; COMMIT;
CREATE MATERIALIZED VIEW jsonview_pure_research_output_external_ids
  BUILD DEFERRED
  REFRESH ON DEMAND
AS
SELECT
  uuid,
  scopus_id,
  qabo_id,
  pmid,
  pmcid,
  orcid
FROM (
  SELECT pi.uuid, jval.*
  FROM
    PURE_JSON_RESEARCH_OUTPUT_516 pi,
    JSON_TABLE(pi.JSON_DOCUMENT, '$'
      COLUMNS(
        NESTED PATH '$.info.additionalExternalIds[*]'
          COLUMNS (
            idSource PATH '$.idSource',
            idValue VARCHAR2(150) PATH '$.value'
          )
      )) jval
    )
    PIVOT (
      MAX(idValue)
      -- Provide aliases inside PIVOT or the columns come out as string names with quotes
      FOR idSource IN ('Scopus' AS scopus_id,'QABO' AS qabo_id,'PubMed' AS pmid,'PubMedCentral' AS pmcid,'ORCID' AS orcid)
    );

CREATE INDEX idx_pure_research_output_external_ids_uuid ON jsonview_pure_research_output_external_ids (uuid);
EXECUTE DBMS_MVIEW.REFRESH('jsonview_pure_research_output_external_ids');
