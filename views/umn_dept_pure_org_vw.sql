CREATE OR REPLACE FORCE EDITIONABLE VIEW expert.umn_dept_pure_org_vw (
  pure_org_id,
  pure_org_uuid,
  pure_org_name, 
  pure_org_type,
  deptid,
  deptid_descr
) AS
WITH pure_org AS (
  SELECT
    org_json.pure_org_id,
    org_table.uuid AS pure_org_uuid,
    org_json.pure_org_name,
    org_json.pure_org_type,
    org_json.id_value AS deptid
  FROM pure_json_organisation_524 org_table
  CROSS APPLY JSON_TABLE(
    org_table.json_document, '$' COLUMNS (
      pure_org_id PATH '$.externalId',
      pure_org_name PATH '$.name.text[0].value',
      pure_org_type PATH '$.type.term.text[0].value',
      NESTED PATH '$.ids[*]' COLUMNS (
        id_type_uri PATH '$.type.uri',
        id_value PATH '$.value.value'
      )
    )
  ) org_json
  WHERE id_type_uri = '/dk/atira/pure/organisation/organisationsources/peoplesoft_deptid'
), umn_dept AS (
  SELECT deptid, deptid_descr, effdt
  FROM (
      SELECT deptid,
             deptid_descr,
             effdt,
             ROW_NUMBER() OVER (PARTITION BY deptid ORDER BY effdt DESC) as rn
      FROM ps_dwhr_job@dweprd.oit
  )
  WHERE rn = 1
)
SELECT
  po.pure_org_id,
  po.pure_org_uuid,
  po.pure_org_name, 
  po.pure_org_type, 
  po.deptid,
  ud.deptid_descr
FROM pure_org po
LEFT JOIN umn_dept ud -- We use a left join here because deptid_descr is just nice to have, not critical.
ON po.deptid = ud.deptid
;
