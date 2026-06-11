CREATE MATERIALIZED VIEW expert.collections_analysis_cited_mvw (
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
)
AS SELECT * FROM expert.collections_analysis_cited_vw;
