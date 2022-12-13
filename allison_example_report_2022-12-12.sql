WITH 
primary_affiliation_org_parents AS (
  SELECT distinct(pss.deptid), po.name_en AS primary_affiliation, hpu.descr AS department, hpu.um_college_descr AS college, hpu.um_campus_descr AS campus
  FROM pure_sync_staff_org_association pss
  JOIN pure_org po ON pss.org_id = po.pure_id
  JOIN hr_ps_um_dpttr_cur_vw@dweprd.oit hpu ON pss.deptid = hpu.deptid
  WHERE pss.primary_association = 1
), 
person_primary_affiliation_data AS (
  SELECT pd.person_id, pd.last_name, pd.first_name, pd.internet_id, soa.deptid, employment_type, 
  CASE
    WHEN soa.period_end_date IS NULL THEN 'Current'
    ELSE 'Not Current'
  END AS employment_status
  FROM pure_sync_staff_org_association soa
  JOIN pure_sync_person_data pd
  ON pd.person_id = soa.person_id
),
person_primary_affiliation_org AS (
  SELECT ppad.person_id, ppad.last_name, ppad.first_name, ppad.internet_id, ppad.employment_status, ppad.employment_type, paop.primary_affiliation, paop.department, paop.college, paop.campus 
  FROM person_primary_affiliation_data ppad
  JOIN primary_affiliation_org_parents paop
  ON ppad.deptid = paop.deptid
)
SELECT
  ro.uuid as pub_uuid,
  ro.json_document.electronicVersions[0].doi as doi,
  ro.json_document.title.value as pub_title,
  ro.json_document.type.term.text[0].value as pub_type,
  ro.json_document.journalAssociation.issn.value as journal_issn,
  ro.json_document.journalAssociation.title.value as journal_title,
  ro.json_document.bibliographicalNote.text[0].value as bibliographical_note,
  --jt.person_id,
  --jt.last_name,
  --jt.first_name
  ppao.last_name, 
  ppao.first_name,
  ppao.internet_id,
  ppao.employment_status,
  ppao.employment_type,
  ppao.primary_affiliation,
  ppao.department, 
  ppao.college, 
  ppao.campus
FROM
  pure_json_research_output_518 ro,
  JSON_TABLE(ro.json_document, '$.personAssociations[*]'
    COLUMNS (
      has_person EXISTS PATH '$.person',
      --person_uuid VARCHAR2(36) PATH '$.person.uuid',
      person_id PATH '$.person.externalId'
      --last_name PATH '$.name.lastName',
      --first_name PATH '$.name.firstName'
    )) jt
  JOIN person_primary_affiliation_org ppao
  ON jt.person_id = ppao.person_id
  WHERE JSON_EXISTS(ro.json_document, '$.personAssociations[*]')
  AND jt.has_person = 'true'
  --FETCH FIRST 100 ROWS ONLY
;
