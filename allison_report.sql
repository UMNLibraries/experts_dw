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
  WHERE soa.primary_association = 1 -- We were missing this the first time! Resulted in duplicate rows.
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
  j.json_document.publisher.name.text[0].value as publisher,
  ro.json_document.type.term.text[0].value as pub_type,
  ro.json_document.journalAssociation.issn.value as journal_issn,
  ro.json_document.journalAssociation.title.value as journal_title,
  ro_publication_state.pub_year AS pub_year,
  ro.json_document.bibliographicalNote.text[0].value as bibliographical_note,
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
  pure_json_research_output_524 ro,
  pure_json_journal_524 j,
  JSON_TABLE(ro.json_document, '$.publicationStatuses[*]'
    COLUMNS (
      is_published EXISTS PATH '$.publicationStatus?(@.uri == "/dk/atira/pure/researchoutput/status/published")',
      --is_epublished EXISTS PATH '$.publicationStatus?(@.uri == "/dk/atira/pure/researchoutput/status/epub")',
      status PATH '$.publicationStatus.term.text[0].value',
      pub_year VARCHAR2(4) PATH '$.publicationDate.year'
    )) ro_publication_state,
  JSON_TABLE(ro.json_document, '$.personAssociations[*]'
    COLUMNS (
      internal_person EXISTS PATH '$.person', -- external persons have key externalPerson
      person_id PATH '$.person.externalId'
    )) ro_person
  JOIN person_primary_affiliation_org ppao
  ON ro_person.person_id = ppao.person_id
  WHERE JSON_EXISTS(ro.json_document, '$.personAssociations[*]')
  AND j.uuid = ro.json_document.journalAssociation.journal.uuid
  AND ro_person.internal_person = 'true'
  AND ro_publication_state.is_published = 'true'
  AND ro_publication_state.pub_year >= 2020
  --FETCH FIRST 100 ROWS ONLY
;
