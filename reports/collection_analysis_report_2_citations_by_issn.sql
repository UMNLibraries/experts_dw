-- Collection Analysis Report #2
-- Row columns: count of umn authors who have cited in the journal, the journal issn

-- This first statement creates a temp table using the following sequence of ctes.
-- Then we query this temp table at the end and group our findings.
-- We are no longer including journal titles because both scopus and pure are unreliable and
-- there are too many duplicates and spelling discrepencies.

CREATE TABLE umn_author_citations_temp
AS
WITH
citation_issns AS (
-- List of distinct citations with journal issn and title
    SELECT DISTINCT
        sjc.scopus_id as CITATION_SCOPUS_ID,
        sjson.issn as ISSN
    FROM
        scopus_json_abstract_cited sjc,
        JSON_TABLE(sjc.json_document, '$."abstracts-retrieval-response".item.bibrecord.head'
            COLUMNS (
                issn    PATH '$.source.issn[0]."$"'
            )) sjson
),
citation_scopus_ids AS (
-- List of author/reference scopus id pairs
    SELECT DISTINCT
        sja.scopus_id as abstract_scopus_id,
        sjson.citation_scopus_id
    FROM
        scopus_json_abstract sja,
        JSON_TABLE(sja.json_document, '$."abstracts-retrieval-response"'
            COLUMNS (
                NESTED PATH '$.item.bibrecord.tail.bibliography.reference[*]' COLUMNS(
                    NESTED PATH '$."ref-info"."refd-itemidlist".itemid[*]' COLUMNS(
                    citation_scopus_id_type PATH '$."@idtype"',
                    citation_scopus_id PATH '$."$"'))
            )) sjson
    WHERE sjson.citation_scopus_id_type = 'SGR' -- SGR is an identifier of a scopus id. We originally discovered this in old SciVerse documentation.
    ORDER BY sja.scopus_id
),

author_scopus_ids AS (
    SELECT DISTINCT
        sja.scopus_id as abstract_scopus_id,
        sjson.author_scopus_id
    FROM
        scopus_json_abstract sja,
        JSON_TABLE(sja.json_document, '$."abstracts-retrieval-response"'
            COLUMNS (
                NESTED PATH '$.authors.author[*]' COLUMNS(
                    author_scopus_id PATH '$."@auid"')
            )) sjson
    ORDER BY sja.scopus_id
),

umn_pure_person_scopus_ids AS (
    -- List of the scopus id of every umn affiliated person in pure_json_person_LATEST_VERSION
    -- Count: 18,174
    SELECT
        sjson.person_scopus_id
    FROM
        pure_json_person_524 pjp,
        JSON_TABLE(pjp.json_document, '$'
            COLUMNS (
                person_id PATH '$.externalId',
                NESTED PATH '$.ids[*]' COLUMNS(
                    person_scopus_id PATH '$.value.value',
                    NESTED PATH '$.type.term.text[*]' COLUMNS(
                    id_type PATH '$.value'))
            )) sjson
    JOIN pure_sync_staff_org_association pssoa
    ON sjson.person_id = pssoa.person_id
    WHERE sjson.id_type = 'Scopus Author ID' AND pssoa.period_end_date is NULL -- do we also want to include period end date within the last three years

-- select count(*) from pure_json_person_524;
-- Count: 56,357
),
-- Join the previous two ctes to filter only umn authors
umn_author_scopus_ids AS (
    SELECT
        asi.abstract_scopus_id,
        asi.author_scopus_id
    FROM
        author_scopus_ids asi
    JOIN umn_pure_person_scopus_ids uppsi
    ON asi.author_scopus_id = uppsi.person_scopus_id
    ORDER BY asi.abstract_scopus_id
),
--select * from umn_author_scopus_ids
umn_author_citations AS (
    SELECT
        uasi.abstract_scopus_id,
        uasi.author_scopus_id,
        csi.citation_scopus_id,
        ci.issn
        --ci.title
    FROM umn_author_scopus_ids uasi
    JOIN citation_scopus_ids csi
    ON uasi.abstract_scopus_id = csi.abstract_scopus_id
    JOIN citation_issns ci
    ON csi.citation_scopus_id = ci.citation_scopus_id
    ORDER BY uasi.abstract_scopus_id
)
--select * from umn_author_citations


--select * from pure_issn_title;

-- The final query of the temp table. Select distinct author scopus ids and group by issn. This shows
-- how many unique u of mn authors have cited a journal in their research during the last three full
-- calendar years.

SELECT count(distinct uact.author_scopus_id) as NUM_UMN_AUTHORS_WHO_CITED_IN, uact.issn as ISSN
FROM umn_author_citations_temp uact
GROUP BY uact.issn
ORDER BY count(distinct uact.author_scopus_id) DESC
;
