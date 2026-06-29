CREATE OR REPLACE FORCE EDITIONABLE VIEW expert.collections_analysis_cited_vw (
  cited_abstract_scopus_id,
  cited_abstract_doi,
  cited_abstract_issn,
  cited_abstract_publication_year,
  authored_abstract_scopus_id,
  author_scopus_id,
  emplid,
  internet_id,
  first_name,
  last_name
) AS
WITH cited AS (
  SELECT
    cited_table.scopus_id AS abstract_scopus_id,
    cited_json.*
  FROM scopus_json_citation cited_table
  CROSS APPLY JSON_TABLE(
    cited_table.json_document, '$."abstract-citations-response"' COLUMNS (
      abstract_doi PATH '$."identifier-legend".identifier[0]."prism:doi"',
      abstract_issn PATH '$.citeInfoMatrix.citeInfoMatrixXML.citationMatrix.citeInfo[0]."prism:issn"',
      abstract_publication_year PATH '$.citeInfoMatrix.citeInfoMatrixXML.citationMatrix.citeInfo[0]."sort-year"'
    )
  ) cited_json
), authored_cited_scopus_ids AS (
  SELECT
    abstract_table.scopus_id as authored_abstract_scopus_id,
    abstract_json.cited_abstract_scopus_id
  FROM scopus_json_abstract abstract_table
  CROSS APPLY JSON_TABLE(
    abstract_table.json_document, '$."abstracts-retrieval-response"' COLUMNS ( 
      NESTED PATH '$.item.bibrecord.tail.bibliography.reference[*]' COLUMNS (
        NESTED PATH '$."ref-info"."refd-itemidlist".itemid[*]' COLUMNS (
          cited_abstract_scopus_id_type PATH '$."@idtype"',
          cited_abstract_scopus_id PATH '$."$"'
        )
      )
    )
  ) abstract_json
  WHERE abstract_json.cited_abstract_scopus_id_type = 'SGR'
)
SELECT
  cited.abstract_scopus_id        AS cited_abstract_scopus_id,
  cited.abstract_doi              AS cited_abstract_doi,
  cited.abstract_issn             AS cited_abstract_issn,
  cited.abstract_publication_year AS cited_abstract_publication_year,
  authored.abstract_scopus_id     AS authored_abstract_scopus_id,
  authored.author_scopus_id       AS author_scopus_id,
  authored.emplid                 AS emplid,
  authored.internet_id            AS internet_id,
  authored.first_name             AS first_name,
  authored.last_name              AS last_name
FROM cited
JOIN authored_cited_scopus_ids acsi
  ON cited.abstract_scopus_id = acsi.cited_abstract_scopus_id
JOIN collections_analysis_authored_mvw authored
  ON authored.abstract_scopus_id = acsi.authored_abstract_scopus_id
;
