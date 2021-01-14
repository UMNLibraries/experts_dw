-- DEPENDS ON:
-- no views

-- DEPENDENTS:
-- no views
DROP MATERIALIZED VIEW jsonview_pub_person;
CREATE MATERIALIZED VIEW jsonview_pub_person
  BUILD DEFERRED
  REFRESH ON DEMAND
AS
SELECT DISTINCT
  p.uuid AS pub_uuid,
  jt.person_pureid,
  -- Internal people come as $.person while external collab as $.externalPerson
  -- Prefer the internal one
  CASE WHEN jt.person_uuid_int IS NOT NULL THEN 'Y' ELSE 'N' END AS person_pure_internal,
  COALESCE(jt.person_uuid_int, jt.person_uuid_ext) AS person_uuid,
  COALESCE(jt.person_link_int, jt.person_link_ext) AS person_link,
  LOWER(jt.person_role) as person_role,
  jt.first_name,
  jt.last_name,
  jt.person_ordinal
FROM PURE_JSON_RESEARCH_OUTPUT_516 p,
    JSON_TABLE(p.JSON_DOCUMENT, '$'
      COLUMNS(
        -- Strangely, using NESTED PATH here instead of just starting with $.personAssociations[*]
        -- in the outer JSON_TABLE() to begin with is MUCH FASTER, 5x faster. Don't understand
        -- why that is, seems like the reverse would be true.
        NESTED PATH '$.personAssociations[*]'
          COLUMNS (
            person_pureid VARCHAR2(36 CHAR) PATH '$.pureId',
            person_uuid_int VARCHAR2(36 CHAR) PATH '$.person.uuid',
            person_uuid_ext VARCHAR2(36 CHAR) PATH '$.externalPerson.uuid',
            person_link_int VARCHAR2(150 CHAR) PATH '$.person.link.href',
            person_link_ext VARCHAR2(150 CHAR) PATH '$.externalPerson.link.href',
            person_role VARCHAR2(255 CHAR) PATH '$.personRole.term.text.value',
            first_name VARCHAR2(1024 CHAR) PATH '$.name.firstName',
            last_name VARCHAR2(1024 CHAR) PATH '$.name.lastName',
            person_ordinal FOR ORDINALITY
          )
    )) jt
;
CREATE INDEX idx_pub_person_pub_uuid_person_uuid ON jsonview_pub_person (pub_uuid, person_uuid);
CREATE INDEX idx_pub_person_pub_person_uuid ON jsonview_pub_person (person_uuid);
EXECUTE DBMS_MVIEW.REFRESH('jsonview_pub_person');