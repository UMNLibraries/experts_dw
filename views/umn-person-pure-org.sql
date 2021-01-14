-- DEPEDNDS ON:
-- pure_org

-- DEPENDENTS:
-- person_pure_org

-- REFRESH TIME (tst): 32s
-- RUN ORDER: 8
DROP MATERIALIZED VIEW jsonview_umn_person_pure_org; COMMIT;
CREATE MATERIALIZED VIEW jsonview_umn_person_pure_org
  BUILD DEFERRED
  REFRESH ON DEMAND
AS
SELECT
  p.uuid AS person_uuid,
  jt.org_uuid AS pure_org_uuid,
  -- Get last segment off URI, remove hyphens because some are non-academic instead of nonacademic
  REPLACE(REVERSE(REGEXP_SUBSTR(REVERSE(jt.staff_type_uri), '[^/]+', 1, 1)), '-', '') AS staff_type,
  jt.job_description,
  jt.employed_as,
  -- iso 8601 with 3 places fractional seconds, timezone as +/-HH:MM
  CAST(TO_TIMESTAMP_TZ(jt.start_date,'YYYY-MM-DD"T"HH24:MI:SS.FF3TZH:TZM') AS DATE) AS start_date,
  CAST(TO_TIMESTAMP_TZ(jt.end_date,'YYYY-MM-DD"T"HH24:MI:SS.FF3TZH:TZM') AS DATE) AS end_date,
  pi.emplid,
  pi.pure_id AS pure_person_id
FROM
  pure_json_person_516 p
  LEFT OUTER JOIN JSON_TABLE(p.JSON_DOCUMENT, '$.staffOrganisationAssociations[*]'
    COLUMNS(
      org_uuid PATH '$.organisationalUnit.uuid',
      staff_type_uri PATH '$.staffType.uri',
      job_description PATH '$.jobDescription[0].text.value',
      -- Technically these should only be the en_US ones, we can drag those out
      -- if really needed. Again XPATH would help here because of JSON_TABLE limitations
      -- Currently ALL are en_US, other locales do not exist in our employmentType data
      employed_as PATH '$.employmentType.term.text[0].value',
      start_date PATH '$.period.startDate',
      end_date PATH '$.period.endDate'
    )) jt ON 1=1
    LEFT OUTER JOIN jsonview_pure_person pi ON p.uuid = pi.uuid AND pi.pure_internal = 'Y'
    -- Only include associations with orgs that are already in Pure
    -- Comment in experts_etl pure_api_internal_person.py:
    -- # If a person has an association with on org not in EDW yet, skip that person...
    INNER JOIN jsonview_pure_org po ON jt.org_uuid = po.uuid
;
CREATE INDEX idx_jsonview_umn_person_pure_org_pure_person_uuid ON jsonview_umn_person_pure_org (person_uuid);
CREATE INDEX idx_jsonview_umn_person_pure_org_pure_org_uuid ON jsonview_umn_person_pure_org (pure_org_uuid);
CREATE INDEX idx_jsonview_umn_person_pure_org_pure_org_emplid ON jsonview_umn_person_pure_org (emplid);
CREATE INDEX idx_jsonview_umn_person_pure_org_pure_org_pure_person_id ON jsonview_umn_person_pure_org (pure_person_id);
EXECUTE DBMS_MVIEW.REFRESH('jsonview_umn_person_pure_org');
