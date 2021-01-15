-- DEPENDS ON:
-- unified_pure_json

-- REFRESH TIME (tst): 369s
-- REFRESH TIME (prd): 145s
-- RUN ORDER: 6
DROP MATERIALIZED VIEW jsonview_pure_person;
CREATE MATERIALIZED VIEW jsonview_pure_person
  BUILD DEFERRED
  REFRESH ON DEMAND
AS
WITH ids AS (
  -- Converts JSON array of person identifiers into columns via PIVOT
  SELECT
    uuid,
    scopus_id,
    scopus_id_ext,
    emplid,
    internet_id
  FROM (
    SELECT p.uuid, jval.*
    FROM
      pure_json_person_516 p,
      JSON_TABLE(p.JSON_DOCUMENT, '$.ids[*]'
        -- Identifiers are denoted by type.uri with a string value
        -- Without PIVOT these would come out as separate rows
        COLUMNS (
          idSource PATH '$.type.uri',
          idValue PATH '$.value.value'
        )) jval
  )
  PIVOT (
    MAX(idValue)
    FOR idSource IN (
      '/dk/atira/pure/person/personsources/scopusauthor' AS scopus_id,
      '/dk/atira/pure/externalperson/externalpersonsources/scopusauthor' AS scopus_id_ext,
      '/dk/atira/pure/person/personsources/employee' AS emplid,
      '/dk/atira/pure/person/personsources/umn' AS internet_id
    )
  )
)
SELECT
  p.uuid,
  jt.pure_id,
  ids.emplid,
  ids.internet_id,
  jt.first_name,
  jt.last_name,
  jt.orcid,
  -- hindex only for internal people
  CASE WHEN p.source = 'pure_json_person' THEN jt.hindex ELSE null END AS hindex,
  COALESCE(ids.scopus_id, ids.scopus_id_ext) AS scopus_id,
  p.pure_modified,
  CASE WHEN p.source = 'pure_json_person' THEN 'Y' ELSE 'N' END AS pure_internal
FROM
  jsonview_unified_pure_json p
  INNER JOIN JSON_TABLE(p.JSON_DOCUMENT, '$'
    COLUMNS (
      -- All internal persons should have this. Usually it will be the same as the emplid,
      -- but sometimes the old SciVal identifier
      pure_id VARCHAR2(1024 CHAR) PATH '$.externalId',
      first_name VARCHAR2(1024 CHAR) PATH '$.name.firstName',
      last_name VARCHAR2(1024 CHAR) PATH '$.name.lastName',
      orcid VARCHAR2(20 CHAR) PATH '$.orcid',
      hindex NUMBER(38,0) PATH '$.scopusHIndex'
    )) jt ON 1=1
    LEFT OUTER JOIN ids ON p.uuid = ids.uuid
WHERE p.source IN ('pure_json_person', 'pure_json_external_person')
;

ALTER TABLE jsonview_pure_person ADD CONSTRAINT pk_pure_person PRIMARY KEY (uuid);
CREATE INDEX jsonview_pure_person_emplid ON jsonview_pure_person (emplid);
CREATE INDEX jsonview_pure_person_internet_id ON jsonview_pure_person (internet_id);
CREATE INDEX jsonview_pure_person_scopus_id ON jsonview_pure_person (scopus_id);
EXECUTE DBMS_MVIEW.REFRESH('jsonview_pure_person');
