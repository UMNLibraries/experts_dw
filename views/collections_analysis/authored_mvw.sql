CREATE MATERIALIZED VIEW expert.collections_analysis_authored_mvw (
  abstract_scopus_id,
  doi,
  issn,
  publication_year,
  author_scopus_id,
  emplid,
  internet_id,
  first_name,
  last_name
)
AS SELECT * FROM expert.collections_analysis_authored_vw;
