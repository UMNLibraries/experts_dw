-- DEPENDS ON:
-- no views

-- DEPENDENTS:
-- no views

-- REFRESH TIME (tst): 2s
-- REFRESH TIME (prd): 10s
-- RUN ORDER: 11
DROP MATERIALIZED VIEW jsonview_umn_dept_pure_org;
CREATE MATERIALIZED VIEW jsonview_umn_dept_pure_org
  BUILD DEFERRED
  REFRESH ON DEMAND
AS
SELECT
  po.uuid AS pure_org_uuid,
  jt.deptid_descr,
  jt.pure_org_id,
  jt.deptid,
  deptid_uri
FROM
  pure_json_organisation_518 po,
  JSON_TABLE(po.JSON_DOCUMENT, '$'
    COLUMNS(
      pure_org_id VARCHAR2(1024) PATH '$.externalId',
      deptid_descr VARCHAR2(255) PATH '$.name.text[0].value',
      NESTED PATH '$.ids[*]'
        COLUMNS(
          deptid VARCHAR2(10) PATH '$.value.value',
          deptid_uri PATH '$.type.uri'
        )
    )) jt
WHERE deptid_uri LIKE '%/peoplesoft_deptid'
;

CREATE INDEX idx_jsonview_umn_dept_pure_org_pure_org_uuid ON jsonview_umn_dept_pure_org (pure_org_uuid);
CREATE INDEX idx_jsonview_umn_dept_pure_org_deptid ON jsonview_umn_dept_pure_org (deptid);
CREATE INDEX idx_jsonview_umn_dept_pure_org_pure_org_id ON jsonview_umn_dept_pure_org (pure_org_id);
EXECUTE DBMS_MVIEW.REFRESH('jsonview_umn_dept_pure_org');
