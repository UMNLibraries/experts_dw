-- New collections analysis reports:

-- Collections Analysis Report 1
-- UMN Authored Abstracts by ISSN
--DROP TABLE collections_analysis_authored;

CREATE TABLE collections_analysis_authored AS
WITH author_metadata AS (
  SELECT DISTINCT
     pspd.emplid,
     pspd.internet_id,
     pspd.first_name,
     pspd.last_name,
     sjson.scopus_id 
  FROM pure_json_person_524 pjp,
    JSON_TABLE (
      pjp.json_document, '$' COLUMNS (
        external_id PATH '$.externalId',
        NESTED PATH '$.ids[*]' COLUMNS (
          scopus_id PATH '$.value.value',
          NESTED PATH '$.type.term.text[*]' COLUMNS (
            author_id_type PATH '$.value'
          )
        )
      )
    ) sjson
  JOIN pure_sync_person_data pspd
    ON sjson.external_id = pspd.person_id
  WHERE sjson.author_id_type = 'Scopus Author ID'
)
SELECT
  sja.scopus_id AS abstract_scopus_id,
  sjson.doi,
  sjson.issn,
  sjson.publication_year,
  sjson.author_scopus_id,
  am.emplid,
  am.internet_id,
  am.first_name,
  am.last_name
FROM scopus_json_abstract_authored sja,
  JSON_TABLE (
    sja.json_document, '$."abstracts-retrieval-response"' COLUMNS (
      doi PATH '$.coredata."prism:doi"',
      issn PATH '$.item.bibrecord.head.source.issn[0]."$"',
      publication_year PATH '$.item.bibrecord.head.source.publicationyear."@first"',
      NESTED PATH '$.authors.author[*]' COLUMNS (
        author_scopus_id PATH '$."@auid"'
      )
    )
  ) sjson
JOIN author_metadata am
  ON sjson.author_scopus_id = am.scopus_id
;

-- Collection Analysis Report 2
-- UMN Cited Abstracts by ISSN
--DROP TABLE collections_analysis_cited;

CREATE TABLE collections_analysis_cited AS
WITH cited_abstract_metadata AS (
  SELECT
    sjc.scopus_id AS cited_abstract_scopus_id,
    sjson.*
  FROM
    scopus_json_abstract_cited sjc,
    JSON_TABLE (
      sjc.json_document, '$."abstracts-retrieval-response"' COLUMNS (
        cited_abstract_doi PATH '$.coredata."prism:doi"',
        cited_abstract_issn PATH '$.item.bibrecord.head.source.issn[0]."$"',
        cited_abstract_publication_year PATH '$.item.bibrecord.head.source.publicationyear."@first"'
      )
    ) sjson
), authored_cited_scopus_ids AS (
  SELECT
    sja.scopus_id as authored_abstract_scopus_id,
    sjson.cited_abstract_scopus_id
  FROM scopus_json_abstract_authored sja,
    JSON_TABLE (
      sja.json_document, '$."abstracts-retrieval-response"' COLUMNS ( 
        NESTED PATH '$.item.bibrecord.tail.bibliography.reference[*]' COLUMNS (
          NESTED PATH '$."ref-info"."refd-itemidlist".itemid[*]' COLUMNS (
            cited_abstract_scopus_id_type PATH '$."@idtype"',
            cited_abstract_scopus_id PATH '$."$"'
          )
        )
      )
    ) sjson
  WHERE sjson.cited_abstract_scopus_id_type = 'SGR'
)
SELECT
  cam.cited_abstract_scopus_id,
  cam.cited_abstract_doi,
  cam.cited_abstract_issn,
  cam.cited_abstract_publication_year,
  caa.abstract_scopus_id AS authored_abstract_scopus_id,
  caa.author_scopus_id,
  caa.emplid,
  caa.internet_id,
  caa.first_name,
  caa.last_name
FROM cited_abstract_metadata cam
JOIN authored_cited_scopus_ids acsi
  ON cam.cited_abstract_scopus_id = acsi.cited_abstract_scopus_id
JOIN collections_analysis_authored caa
  ON caa.abstract_scopus_id = acsi.authored_abstract_scopus_id
;
