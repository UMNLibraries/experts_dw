-- View converting publication externalIds to columns indexed by UUID
-- Use for joining to other queries and getting a flat view of other identifiers

-- DEPEDNDS ON:
-- no views

-- DEPENDENTS VIEWS:
-- pure_research_output_pub
DROP MATERIALIZED VIEW jsonview_pure_research_output_pubdates; COMMIT;
CREATE MATERIALIZED VIEW jsonview_pure_research_output_pubdates
  BUILD DEFERRED
  REFRESH ON DEMAND
AS
SELECT
  uuid,
  issued,
  issued_is_current AS issued_current,
  issued_precision,
  eissued,
  eissued_is_current AS eissued_current,
  eissued_precision,
  unissued,
  unissued_is_current AS unissued_current,
  unissued_precision,
  inprep,
  inprep_is_current AS inprep_current,
  inprep_precision,
  submitted,
  submitted_is_current AS submitted_current,
  submitted_precision,
  COALESCE(in_press, inpress) AS inpress,
  COALESCE(in_press_is_current, inpress_is_current) AS inpress_current,
  COALESCE(in_press_precision, inpress_precision) AS inpress_precision
FROM
(
  SELECT pi.uuid,
  REVERSE(REGEXP_SUBSTR(REVERSE(jval.pubstatus), '[^/]+', 1, 1)) AS publication_status,
  CASE WHEN jval.pubyear IS NOT NULL THEN TO_DATE(jval.pubyear || '-' || COALESCE(jval.pubmonth,'1') || '-' || COALESCE(jval.pubday,'1'), 'YYYY-mm-dd') ELSE NULL END AS pubdate,
  CASE
    WHEN jval.pubyear IS NOT NULL AND jval.pubmonth IS NULL THEN 366
    WHEN jval.pubyear IS NOT NULL AND jval.pubmonth IS NOT NULL AND jval.pubday IS NULL THEN 31
    WHEN jval.pubyear IS NOT NULL AND jval.pubmonth IS NOT NULL AND jval.pubday IS NOT NULL THEN 1
  END AS precision,
  jval.is_current
  FROM
    PURE_JSON_RESEARCH_OUTPUT_516 pi,
    JSON_TABLE(pi.JSON_DOCUMENT, '$'
      COLUMNS(
        NESTED PATH '$.publicationStatuses[*]'
          COLUMNS (
           pubyear PATH '$.publicationDate.year',
            pubmonth PATH '$.publicationDate.month',
            pubday PATH '$.publicationDate.day',
            is_current PATH '$.current',
            pubstatus PATH '$.publicationStatus.uri'
          )
      )) jval
    )
    PIVOT (
      -- You can pivot on 2 columns, and Oracle will append the supplied alias with an underscore
      -- therefore these come out as issued, issued_is_current, issued_precision, eissued, eissued_is_current, eissued_precision....
      -- (but "current" is a keyword and quoting makes it behave weirdly, so we can just fix the aliases
      -- ini the outer SELECT to be issued_current without the _is
      -- example https://stackoverflow.com/a/23939719/541091
      MAX(pubdate), MAX(is_current) as is_current, MAX(precision) AS precision
      -- Provide aliases inside PIVOT or the columns come out as string names with quotes
      FOR publication_status IN ('published' AS issued, 'epub' AS eissued, 'unpublished' AS unissued, 'inprep' AS inprep, 'submitted' AS submitted, 'in_press' AS in_press, 'inpress' AS inpress)
    )
;
CREATE INDEX idx_pure_research_output_pubdates_uuid ON jsonview_pure_research_output_pubdates (uuid);
EXECUTE DBMS_MVIEW.REFRESH('jsonview_pure_research_output_pubdates');
