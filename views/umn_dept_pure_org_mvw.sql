CREATE MATERIALIZED VIEW expert.umn_dept_pure_org_mvw (
  pure_org_id,
  pure_org_uuid,
  pure_org_name, 
  pure_org_type,
  deptid,
  deptid_descr
)
AS SELECT * FROM expert.umn_dept_pure_org_vw;
CREATE INDEX ix_umn_dept_pure_org_mvw_deptid ON umn_dept_pure_org_mvw (deptid);
