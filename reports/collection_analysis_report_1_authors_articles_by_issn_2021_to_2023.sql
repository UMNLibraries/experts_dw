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
    WHERE sjson.affiliation = '60008772'
    GROUP BY sjson.issn
    ORDER BY sjson.issn
),
--select * from scopus_ids;

abstract_authors AS (
    SELECT DISTINCT
        --sja.scopus_id as SCOPUS_ID,
        sjson.issn as ISSN,
        --sjson.type as TYPE,
        --sjson.source_title as TITLE,
        sjson.author_id
        --sjson.issn || sjson.author_id as UNIQUE_AUTHOR
        --count(sjson.author_id) as AUTHOR_ID
    FROM
        scopus_json_abstract_authored sja,
        JSON_TABLE(sja.json_document, '$."abstracts-retrieval-response".item.bibrecord.head'
            COLUMNS (
                issn    PATH '$.source.issn[0]."$"',
                --type    PATH '$.source.issn[0]."@type"',
                --source_title  PATH '$.source.sourcetitle',
                NESTED PATH '$."author-group"[*]' COLUMNS(
                    affiliation PATH '$.affiliation."@afid"',
                    NESTED PATH '$.author[*]' COLUMNS(author_id PATH '$."@auid"'))
            )) sjson
    WHERE sjson.affiliation = '60008772'
    --GROUP BY sja.scopus_id, sjson.issn, sjson.affiliation
    --ORDER BY sjson.issn, sjson.author_id
    --FETCH FIRST 1000 ROWS ONLY
),
--select * from abstract_authors; -- will take 45-60 seconds

unique_authors_list AS (
    SELECT issn, count(author_id) AS unique_authors
    FROM abstract_authors
    GROUP BY issn
    ORDER BY issn
),

pure_issn_title AS (
    SELECT
        REGEXP_REPLACE(sjson.issn, '-', '') as issn,
        listagg(distinct sjson.title, ',' ON OVERFLOW TRUNCATE) as journal_title     
    FROM
        pure_json_journal_524 pjj,
        JSON_TABLE(pjj.json_document, '$'
        COLUMNS (
            title PATH '$.titles[0].value',
            NESTED PATH '$.issns[*]' COLUMNS (
                issn PATH '$.value')
        )) sjson
GROUP BY sjson.issn
ORDER BY sjson.issn    
)

SELECT ul.issn, s.number_of_articles, s.number_of_authors, ul.unique_authors, s.article_scopus_ids, s.author_scopus_ids
FROM unique_authors_list ul
LEFT JOIN scopus_ids s
ON ul.issn = s.issn
ORDER BY ul.issn
--1,420 rows
;
