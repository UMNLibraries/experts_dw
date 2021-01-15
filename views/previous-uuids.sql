-- DEPENDS ON:
-- unified_pure_json

-- REFRESH TIME (tst): 491s
-- REFRESH TIME (prd): 526s
-- RUN ORDER: 10

DROP MATERIALIZED VIEW jsonview_previous_uuid; COMMIT;
CREATE MATERIALIZED VIEW jsonview_previous_uuid
  BUILD DEFERRED
  REFRESH ON DEMAND
AS
SELECT
  p.uuid,
  jt.previous_uuid
FROM
  jsonview_unified_pure_json p,
  JSON_TABLE(p.JSON_DOCUMENT, '$.info.previousUuids[*]'
    COLUMNS (
      previous_uuid VARCHAR2(36) PATH '$'
    )) jt
  WHERE JSON_EXISTS(p.JSON_DOCUMENT, '$.info.previousUuids[*]')

;
ALTER TABLE jsonview_previous_uuid ADD CONSTRAINT pk_uuid_previous_uuid PRIMARY KEY (uuid, previous_uuid);
EXECUTE DBMS_MVIEW.REFRESH('jsonview_previous_uuid');
