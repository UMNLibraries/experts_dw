-- Collection Analysis Report 1
-- Shows number of articles and authors (total and unique) grouped and ordered by ISSN
WITH
scopus_ids AS (
    SELECT
        sjson.issn as ISSN,
        count(sjson.author_id) as number_of_authors,
        count(distinct sja.scopus_id) as number_of_articles,
        listagg(distinct sja.scopus_id, ',') as article_scopus_ids,
        listagg(distinct sjson.author_id, ',') as author_scopus_ids
    FROM
        scopus_json_abstract_authored sja,
        JSON_TABLE(sja.json_document, '$."abstracts-retrieval-response".item.bibrecord.head'
            COLUMNS (
                issn    PATH '$.source.issn[0]."$"',
                source  PATH '$.source.sourcetitle',
                NESTED PATH '$."author-group"[*]' COLUMNS(
                    affiliation PATH '$.affiliation."@afid"',
                    NESTED PATH '$.author[*]' COLUMNS(author_id PATH '$."@auid"'))
            )) sjson
    GROUP BY sjson.issn
    ORDER BY sjson.issn
),
--select * from scopus_ids;

abstract_authors AS (
    SELECT DISTINCT
        sjson.issn as ISSN,
        sjson.author_id
    FROM
        scopus_json_abstract_authored sja,
        JSON_TABLE(sja.json_document, '$."abstracts-retrieval-response".item.bibrecord.head'
            COLUMNS (
                issn    PATH '$.source.issn[0]."$"',
                NESTED PATH '$."author-group"[*]' COLUMNS(
                    NESTED PATH '$.author[*]' COLUMNS(author_id PATH '$."@auid"'))
            )) sjson
),
select * from abstract_authors; -- will take 45-60 seconds

unique_authors_list AS (
    SELECT issn, count(author_id) AS unique_authors
    FROM abstract_authors
    GROUP BY issn
    ORDER BY issn
),

final_articles_and_authors AS (
  SELECT ul.issn, s.number_of_articles, s.number_of_authors, ul.unique_authors, s.article_scopus_ids, s.author_scopus_ids
  FROM unique_authors_list ul
  LEFT JOIN scopus_ids s
  ON ul.issn = s.issn
  ORDER BY ul.issn
)
select * from final_articles_and_authors
;
