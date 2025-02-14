-- Collections Analysis Reports Combined
-- SQL for creating temporary tables and running two final reports:
-- 1. UMN Authored Articles by ISSN
-- 2. UMN Cited Articles by ISSN
-- Assumes the availability of scopus_json_abstract_authored and scopus_json_abstract_cited tables.

-- Temp Table 1
-- umn_cited_abstract_ids
-- Contains cited abstract scopus id, publication year, issn, and doi.
-- DROP TABLE umn_cited_abstract_ids;

CREATE TABLE umn_cited_abstract_ids AS
    SELECT
      sjc.scopus_id AS cited_abstract_scopus_id,
      sjson.cited_abstract_year,
      sjson.issn AS cited_abstract_issn,
      sjson.doi AS cited_abstract_doi
    FROM
      scopus_json_abstract_cited sjc,
      JSON_TABLE (
        sjc.json_document, '$."abstracts-retrieval-response"'
        COLUMNS (
          cited_abstract_year PATH '$.item.bibrecord.head.source.publicationyear."@first"',
          issn PATH '$.item.bibrecord.head.source.issn[0]."$"',
          doi PATH '$.coredata."prism:doi"'
        )
      ) sjson
;

-- Temp Table 2 
-- umn_authored_abstract_cited_scopus_ids
-- Two column table matching the authored_abstract to its cited_abstracts
--DROP TABLE umn_authored_abstract_cited_scopus_ids;

CREATE TABLE umn_authored_abstract_cited_scopus_ids AS
SELECT
      sja.scopus_id as authored_abstract_scopus_id,
      sjson.cited_abstract_scopus_id
    FROM
      scopus_json_abstract_authored sja,
      JSON_TABLE (
        sja.json_document, '$."abstracts-retrieval-response"'
          COLUMNS (
            NESTED PATH '$.item.bibrecord.tail.bibliography.reference[*]' COLUMNS (
              NESTED PATH '$."ref-info"."refd-itemidlist".itemid[*]' COLUMNS (
                cited_abstract_scopus_id_type PATH '$."@idtype"',
                cited_abstract_scopus_id PATH '$."$"'
              )
            )
          )
      ) sjson
    WHERE sjson.cited_abstract_scopus_id_type = 'SGR' 
;

-- Temp Table 3
-- umn_authored_abstract_author_scopus_ids
-- Two column table matching the abstract's scopus id with an author's scopus id
--DROP TABLE umn_authored_abstract_author_scopus_ids;

CREATE TABLE umn_authored_abstract_author_scopus_ids AS
    SELECT
      sja.scopus_id as authored_abstract_scopus_id,
      sjson.author_scopus_id
    FROM
      scopus_json_abstract_authored sja,
      JSON_TABLE (
        sja.json_document, '$."abstracts-retrieval-response"'
        COLUMNS (
          NESTED PATH '$.authors.author[*]' COLUMNS (
            author_scopus_id PATH '$."@auid"'
          )
        )
      ) sjson
;

-- Temp Table 4
-- UMN_PURE_PERSON_IDS
-- Matches author scopus id to emplid, internet_id, first_name, last_name
--DROP TABLE UMN_PURE_PERSON_IDS;

CREATE TABLE UMN_PURE_PERSON_IDS AS 
 SELECT DISTINCT
    pspd.emplid,
    pspd.internet_id,
    pspd.first_name,
    pspd.last_name,
    sjson.author_id AS author_scopus_id
  FROM
    pure_json_person_524 pjp,
    JSON_TABLE (
      pjp.json_document, '$'
      COLUMNS (
        external_id PATH '$.externalId',
        NESTED PATH '$.ids[*]' COLUMNS (
          author_id PATH '$.value.value',
          NESTED PATH '$.type.term.text[*]' COLUMNS (
            author_id_type PATH '$.value'
          )
        )
      )
    ) sjson
  JOIN pure_sync_person_data pspd
  ON sjson.external_id = pspd.person_id
  WHERE sjson.author_id_type = 'Scopus Author ID'
  ;
  
-- Temp Table 5
-- umn_author_ids
-- Matches the authored abstract scopus id to author scopus id and author metadata (emplid, internet_id, f/l name)
--DROP TABLE umn_author_ids;

CREATE TABLE umn_author_ids AS
    SELECT
      asi.authored_abstract_scopus_id,
      uppi.author_scopus_id,
      uppi.emplid,
      uppi.internet_id,
      uppi.first_name,
      uppi.last_name
    FROM umn_authored_abstract_author_scopus_ids asi
    JOIN umn_pure_person_ids uppi
    ON asi.author_scopus_id = uppi.author_scopus_id
;

-- Collection Analysis Report 1
-- U of MN Authored Abstracts by ISSN 
-- This code needs updating to reflect new metadata and temp tables.
CREATE TABLE umn_scopus_articles_authors_by_issn
AS
WITH
scopus_ids AS (
    SELECT
        sjson.doi,
        sjson.issn as ISSN,
        sja.scopus_id as ARTICLE_SCOPUS_ID,
        sjson.author_scopus_id
    FROM
        scopus_json_abstract_authored sja,
        JSON_TABLE(sja.json_document, '$."abstracts-retrieval-response"'
            COLUMNS (
                doi PATH '$.coredata."prism:doi"',
                issn    PATH '$.item.bibrecord.head.source.issn[0]."$"',
                NESTED PATH '$.item.bibrecord.head."author-group"[*]' COLUMNS(
                    NESTED PATH '$.author[*]' COLUMNS(author_scopus_id PATH '$."@auid"'))
            )) sjson
    ORDER BY sjson.issn
)

SELECT
  si.issn as ISSN,
  si.article_scopus_id,
  si.author_scopus_id,
  si.doi as ARTICLE_DOI,
  uppi.emplid as EMPLID
FROM scopus_ids si
JOIN umn_pure_person_ids uppi
ON si.author_scopus_id = uppi.author_scopus_id
ORDER BY si.issn
;

-- Collection Analysis Report 2
-- U of MN Cited Abstracts by ISSN 
--drop table umn_scopus_cited_articles_authors_by_issn;

CREATE TABLE umn_scopus_cited_articles_authors_by_issn AS

SELECT
  ci.cited_abstract_issn,
  ci.cited_abstract_doi,
  ci.cited_abstract_year,
  csi.cited_abstract_scopus_id,
  uai.authored_abstract_scopus_id,
  uai.author_scopus_id,
  uai.emplid,
  uai.internet_id,
  uai.first_name,
  uai.last_name
FROM umn_author_ids uai
JOIN umn_authored_abstract_cited_scopus_ids csi
ON uai.authored_abstract_scopus_id = csi.authored_abstract_scopus_id
JOIN umn_cited_abstract_ids ci
ON csi.cited_abstract_scopus_id = ci.cited_abstract_scopus_id
;







