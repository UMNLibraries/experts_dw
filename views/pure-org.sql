DROP MATERIALIZED VIEW jsonview_pure_org; COMMIT;
CREATE MATERIALIZED VIEW jsonview_pure_org
  BUILD DEFERRED
  REFRESH ON DEMAND
AS
SELECT
  p.uuid,
  CASE WHEN jou.externalIdSource = 'synchronisedUnifiedOrganisation' THEN jou.pure_id ELSE NULL END AS pure_id,
  jou.parent_pure_uuid,
  CASE WHEN jou.parent_externalIdSource = 'synchronisedUnifiedOrganisation' THEN jou.parent_pure_id ELSE NULL END AS parent_pure_id,
  CASE WHEN p.source = 'pure_json_organisation' THEN 'Y' ELSE 'N' END AS pure_internal,
  REVERSE(REGEXP_SUBSTR(REVERSE(jou.type_uri), '[^/]+', 1, 1)) AS type,
  CASE WHEN jou.name_locale = 'en_US' THEN name ELSE NULL END AS name_en,
  jou.name_variant_en,
  jou.url,
  p.pure_modified
FROM jsonview_unified_pure_json p,
  JSON_TABLE(p.JSON_DOCUMENT, '$'
    COLUMNS(
      uuid PATH '$.uuid',
      pure_id PATH '$.externalId',
      externalIdSource PATH '$.externalIdSource',
      parent_pure_uuid PATH '$.parents[0].uuid',
      parent_pure_id PATH '$.parents[0].externalId',
      parent_externalIdSource PATH '$.parents[0].externalIdSource',
      type_uri PATH '$.type.uri',
      name_locale PATH '$.name.text.locale',
      name PATH '$.name.text.value',
      -- Bogus value, we do not populate this column anymore, but Oracle will not allow
      -- a literal NULL as a view column so this will just pass a null up to SELECT
      -- and we can always uncomment it later if we want it.
      name_variant_en PATH '$.nameVariants[0].value.text.value.BOGUS',
      url PATH '$.webAddresses[0].value.text.value.BOGUS'
    )) jou
WHERE p.source IN ('pure_json_organisation','pure_json_external_organisation')
;

CREATE INDEX idx_pure_org_uuid ON jsonview_pure_org (uuid);
CREATE INDEX idx_pure_org_pure_id ON jsonview_pure_org (pure_id);
EXECUTE DBMS_MVIEW.REFRESH('jsonview_pure_org');