CREATE OR REPLACE FORCE EDITIONABLE VIEW expert.collections_analysis_authored_vw (
  abstract_scopus_id,
  doi,
  issn,
  publication_year,
  author_scopus_id,
  emplid,
  internet_id,
  first_name,
  last_name
) AS 
WITH author AS (
  SELECT DISTINCT
    umn.emplid,
    umn.internet_id,
    umn.first_name,
    umn.last_name,
    pure.scopus_id 
  FROM pure_json_person_524 pjp
  CROSS APPLY JSON_TABLE(
      pjp.json_document, '$' COLUMNS (
        external_id PATH '$.externalId',
        NESTED PATH '$.ids[*]' COLUMNS (
          scopus_id PATH '$.value.value',
          NESTED PATH '$.type.term.text[*]' COLUMNS (
            author_id_type PATH '$.value'
          )
        )
      )
    ) pure
  JOIN pure_sync_person_data umn
    ON pure.external_id = umn.person_id
  WHERE pure.author_id_type = 'Scopus Author ID'
)
SELECT
  abstract_table.scopus_id       AS abstract_scopus_id,
  abstract_json.doi              AS doi,
  abstract_json.issn             AS issn,
  abstract_json.publication_year AS publication_year,
  abstract_json.author_scopus_id AS author_scopus_id,
  author.emplid                  AS emplid,
  author.internet_id             AS internet_id,
  author.first_name              AS first_name,
  author.last_name               AS last_name
FROM scopus_json_abstract abstract_table
CROSS APPLY JSON_TABLE(
    abstract_table.json_document, '$."abstracts-retrieval-response"' COLUMNS (
      doi PATH '$.coredata."prism:doi"',
      issn PATH '$.item.bibrecord.head.source.issn[0]."$"',
      publication_year PATH '$.item.bibrecord.head.source.publicationyear."@first"',
      NESTED PATH '$.authors.author[*]' COLUMNS (
        author_scopus_id PATH '$."@auid"'
      )
    )
  ) abstract_json
JOIN author
  ON abstract_json.author_scopus_id = author.scopus_id
;
