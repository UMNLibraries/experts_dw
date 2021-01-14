-- DEPEDNDS ON:
-- pure_research_output_pubdates
-- pure_research_output_doi
-- pure_research_output_external_ds
-- PURE_JSON_RESEARCH_OUTPUT_516

-- DEPENDENTS:
-- no views

DROP MATERIALIZED VIEW jsonview_pub; COMMIT;
CREATE MATERIALIZED VIEW jsonview_pub
  BUILD DEFERRED
  REFRESH ON DEMAND
AS
SELECT
  p.uuid,
  jt.pureId,
  -- Scopus ID was retrieved from externalId in experts_etl - it is also present in externalIds[]
  -- so get it first from the former, default to the latter
  COALESCE(CASE WHEN jt.externalIdSource = 'Scopus' THEN jt.externalId ELSE NULL END, ids.scopus_id) AS scopus_id,
  jt.title,
  jt.container_title,
  jt.journal_uuid,
  jt.issn,
  jt.volume,
  jt.pages,
  jt.issue,
  jt.citation_total,
  jt.owner_pure_org_id,
  p.pure_modified,
  -- jt.type, -- PUB.type is deprecated in experts_etl "commented out because we will rely more on pure types and subtypes"
  -- Flip the URI, get the second (second last before flip) slash-delim component, and flip it back
  -- Easier to do this on a reversed string because it regexp_substr supports match positions but we may not
  -- know the total number of /-delim segments
  REVERSE(REGEXP_SUBSTR(REVERSE(jt.types_uri), '[^/]+', 1, 2)) AS pure_type,
  -- Same, but with the last (first) component as subtype
  REVERSE(REGEXP_SUBSTR(REVERSE(jt.types_uri), '[^/]+', 1, 1)) AS pure_subtype,
  d.issued,
  d.issued_current,
  d.issued_precision,
  d.eissued,
  d.eissued_current,
  d.eissued_precision,
  d.unissued,
  d.unissued_current,
  d.unissued_precision,
  d.inprep,
  d.inprep_current,
  d.inprep_precision,
  d.submitted,
  d.submitted_current,
  d.submitted_precision,
  d.inpress,
  d.inpress_current,
  d.inpress_precision,
  doi.doi,
  doi.doi_openaccess,
  ids.qabo_id,
  ids.pmid,
  ids.pmcid,
  ids.orcid
FROM
  PURE_JSON_RESEARCH_OUTPUT_516 p
  -- Instead of the implicit join behavior, to join additional tables it has to be explicit
  -- inner joins here. Cannot use the simple comma-separated "tablename t, JSON_TABLE(t.json_doc....) jt"
  -- syntax if we have other joins to make
  INNER JOIN JSON_TABLE(p.JSON_DOCUMENT, '$'
    COLUMNS (
      pureId VARCHAR2(36) PATH '$.pureId',
      externalIdSource PATH '$.externalIdSource',
      externalId PATH '$.externalId',
      owner_pure_org_id PATH '$.managingOrganisationalUnit.uuid',
      title PATH '$.title.value',
      container_title PATH '$.journalAssociation.journal.name.text.value',
      journal_uuid PATH '$.journalAssociation.journal.uuid',
      issn PATH '$.journalAssociation.issn.value',
      volume PATH '$.volume',
      issue PATH '$.journalNumber',
      pages PATH '$.pages',
      citation_total PATH '$.totalScopusCitations',
      types_uri PATH '$.type.uri'
    )
  ) jt ON 1=1
  -- Hook up all the other dependent views which flattened various nested JSON array structures
  LEFT OUTER JOIN jsonview_pure_research_output_pubdates d ON p.uuid = d.uuid
  LEFT OUTER JOIN jsonview_pure_research_output_external_ids ids ON p.uuid = ids.uuid
  LEFT OUTER JOIN jsonview_pure_research_output_doi doi ON p.uuid = doi.uuid
;
ALTER TABLE jsonview_pub ADD CONSTRAINT pk_jsonview_pub PRIMARY KEY (uuid);
CREATE INDEX jsonview_pub_doi ON jsonview_pub (doi);
CREATE INDEX jsonview_pub_scopus_id ON jsonview_pub (scopus_id);
CREATE INDEX jsonview_pub_orcid ON jsonview_pub (orcid);
EXECUTE DBMS_MVIEW.REFRESH('jsonview_pub');
