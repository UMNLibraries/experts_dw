-- :name latest_pure_api_changes_for_family :many
SELECT c1.uuid, c1.change_type, c1.version, c1.family_system_name
FROM pure_api_change c1
LEFT JOIN pure_api_change c2
ON c1.uuid = c2.uuid
AND c1.version < c2.version
WHERE c2.version IS NULL
AND c1.family_system_name = :family_system_name
