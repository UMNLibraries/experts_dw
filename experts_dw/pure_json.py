from datetime import datetime
import functools
import json
from typing import Any, Callable, MutableMapping, Tuple, TypeVar, cast

import cx_Oracle

from experts_dw import db
from experts_dw.exceptions import ExpertsDwException
from experts_dw.pure_json_collection_meta import ChangeMeta, CollectionMeta

iso_8601_format = '%Y-%m-%dT%H:%M:%S.%f%z'

def document_exists(
    cursor:cx_Oracle.Cursor,
    *,
    uuid:str,
    meta:CollectionMeta,
    staging:bool=False
):
    collection_table_name = meta.staging_table_name if staging else meta.canonical_table_name
    cursor.execute(
        f'SELECT count(*) FROM {collection_table_name} WHERE uuid = :uuid',
        {'uuid': uuid}
    )
    document_count = cursor.fetchone()[0] # Result will be a tuple
    if document_count > 0:
        return True
    else:
        return False

def insert_sql(
    *,
    meta:CollectionMeta,
    staging:bool=False
):
    collection_table_name = meta.staging_table_name if staging else meta.canonical_table_name
    primary_key_column_names = 'uuid'
    primary_key_predicate = 'uuid = :uuid'
    if staging:
        primary_key_column_names = primary_key_column_names + ', pure_modified'
        primary_key_predicate = primary_key_predicate + ' AND pure_modified = :pure_modified'
    return f'''
        INSERT /*+ ignore_row_on_dupkey_index({collection_table_name}({primary_key_column_names})) */ 
        INTO {collection_table_name}
        (
          uuid,
          pure_created,
          pure_modified,
          inserted,
          updated,
          json_document
        ) VALUES (
          :uuid,
          :pure_created,
          :pure_modified,
          :inserted,
          :updated,
          :json_document
        )
    '''

def insert_document(
    cursor:cx_Oracle.Cursor,
    *,
    document:MutableMapping,
    meta:CollectionMeta,
    staging:bool=False
):
    sql = insert_sql(
        meta=meta,
        staging=staging
    )
    cursor.execute(sql, document)

def insert_documents(
    cursor:cx_Oracle.Cursor,
    *,
    documents:list[MutableMapping],
    meta:CollectionMeta,
    staging:bool=False
):
    sql = insert_sql(
        meta=meta,
        staging=staging
    )
    cursor.executemany(sql, documents)

def max_change_history_inserted_date(
    cursor:cx_Oracle.Cursor,
    *,
    meta:ChangeMeta
):
    cursor.execute(
        f'SELECT MAX(inserted) FROM {meta.history_table_name}'
    )
    return cursor.fetchone()[0] # Result will be a tuple

def max_change_inserted_date(
    cursor:cx_Oracle.Cursor,
    *,
    meta:ChangeMeta
):
    cursor.execute(
        f'SELECT MAX(inserted) FROM {meta.buffer_table_name}'
    )
    return cursor.fetchone()[0] # Result will be a tuple

def max_pure_version_for_change_history_uuid(
    cursor:cx_Oracle.Cursor,
    *,
    uuid:str,
    meta:ChangeMeta
):
    cursor.execute(
        f'SELECT MAX(pure_version) FROM {meta.history_table_name} WHERE uuid = :uuid',
        {'uuid': uuid}
    )
    return cursor.fetchone()[0] # Result will be a tuple

def max_pure_version_for_change_uuid(
    cursor:cx_Oracle.Cursor,
    *,
    uuid:str,
    meta:ChangeMeta
):
    cursor.execute(
        f'SELECT MAX(pure_version) FROM {meta.buffer_table_name} WHERE uuid = :uuid',
        {'uuid': uuid}
    )
    return cursor.fetchone()[0] # Result will be a tuple

def change_document_exists(
    cursor:cx_Oracle.Cursor,
    *,
    uuid:str,
    pure_version:str,
    meta:ChangeMeta
):
    cursor.execute(
        f'SELECT count(*) FROM {meta.buffer_table_name} WHERE uuid = :uuid AND pure_version = :pure_version',
        {'uuid': uuid, 'pure_version': pure_version}
    )
    document_count = cursor.fetchone()[0] # Result will be a tuple
    if document_count > 0:
        return True
    else:
        return False

def change_history_exists(
    cursor:cx_Oracle.Cursor,
    *,
    uuid:str,
    pure_version:str,
    meta:ChangeMeta
):
    cursor.execute(
        f'SELECT count(*) FROM {meta.history_table_name} WHERE uuid = :uuid AND pure_version = :pure_version',
        {'uuid': uuid, 'pure_version': pure_version}
    )
    history_count = cursor.fetchone()[0] # Result will be a tuple
    if history_count > 0:
        return True
    else:
        return False

def insert_change_sql(
    *,
    meta:ChangeMeta
):
    return f'''
        INSERT /*+ ignore_row_on_dupkey_index({meta.buffer_table_name}(uuid, pure_version)) */ 
        INTO {meta.buffer_table_name}
        (
          uuid,
          pure_version,
          change_type,
          family_system_name,
          inserted,
          json_document
        ) VALUES (
          :uuid,
          :pure_version,
          :change_type,
          :family_system_name,
          :inserted,
          :json_document
        )
    '''

def insert_change_documents(
    cursor:cx_Oracle.Cursor,
    *,
    documents:list[MutableMapping],
    meta:ChangeMeta
):
    sql = insert_change_sql(
        meta=meta
    )
    cursor.executemany(sql, documents)

def delete_documents_based_on_changes_sql(
    *,
    meta:CollectionMeta,
):
    # Not bothering to check for max(pure_version) here because historically
    # DELETEs have always been the max version.
    return f'''
        DELETE FROM {meta.canonical_table_name}
        WHERE uuid IN (
          SELECT uuid FROM {meta.change_meta.buffer_table_name}
          WHERE change_type = 'DELETE'
          AND family_system_name = '{meta.family_system_name}'
        )
    '''

def delete_documents_based_on_changes(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    sql = delete_documents_based_on_changes_sql(
        meta=meta,
    )
    cursor.execute(sql)

def insert_change_deletes_history_sql(
    *,
    meta:CollectionMeta,
):
    return f'''
        MERGE INTO {meta.change_meta.history_table_name} pjh
        USING (
          SELECT
            uuid,
            pure_version,
            family_system_name,
            change_type,
            inserted
          FROM {meta.change_meta.buffer_table_name}
          WHERE
            change_type = 'DELETE'
            AND pj.family_system_name = '{meta.family_system_name}'
        )
        ON (pj.uuid = pjh.uuid AND pj.pure_version = pjh.pure_version)
        WHEN NOT MATCHED THEN
          INSERT (pjh.uuid, pjh.pure_version, pjh.family_system_name, pjh.change_type, pjh.inserted)
          VALUES (pj.uuid, pj.pure_version, pj.family_system_name, pj.change_type, pj.inserted)
    '''

def insert_change_deletes_history(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    sql = insert_change_deletes_history_sql(
        meta=meta,
    )
    cursor.execute(sql)

def delete_change_deletes_sql(
    *,
    meta:CollectionMeta,
):
    return f'''
        DELETE FROM {meta.change_meta.buffer_table_name}
        WHERE change_type = 'DELETE'
        AND family_system_name = '{meta.family_system_name}'
    '''

def delete_change_deletes(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    sql = delete_change_deletes_sql(
        meta=meta,
    )
    cursor.execute(sql)

def process_change_deletes(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    connection = cursor.connection
    connection.begin()

    try:
        delete_documents_based_on_changes(
            cursor,
            meta=meta,
        )

        insert_change_deletes_history(
            cursor,
            meta=meta,
        )

        delete_change_deletes(
            cursor,
            meta=meta,
        )
    except Exception as e:
        connection.rollback()
        raise e

    connection.commit()

def insert_change_history_matching_previous_uuids_sql(
    *,
    meta:CollectionMeta,
):
    return f'''
        MERGE INTO {meta.change_meta.history_table_name} pjh
        USING (
          SELECT
            uuid,
            pure_version,
            family_system_name,
            change_type,
            inserted
          FROM {meta.change_meta.buffer_table_name}
          WHERE uuid IN (
            SELECT jt.previous_uuid
            FROM {meta.canonical_table_name},
              JSON_TABLE(json_document, '$'
                COLUMNS (
                  uuid VARCHAR2(36) PATH '$.uuid',
                  NESTED PATH '$.info.previousUuids[*]'
                    COLUMNS (
                      previous_uuid VARCHAR2(36) PATH '$'
                    )
                )
              )
              AS jt
              WHERE JSON_EXISTS(json_document, '$.info.previousUuids') AND jt.previous_uuid IS NOT NULL
          )
        ) pj
        ON (pj.uuid = pjh.uuid AND pj.pure_version = pjh.pure_version)
        WHEN NOT MATCHED THEN
          INSERT (pjh.uuid, pjh.pure_version, pjh.family_system_name, pjh.change_type, pjh.inserted)
          VALUES (pj.uuid, pj.pure_version, pj.family_system_name, pj.change_type, pj.inserted)
    '''

def insert_change_history_matching_previous_uuids(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    sql = insert_change_history_matching_previous_uuids_sql(
        meta=meta,
    )
    cursor.execute(sql)

def delete_changes_matching_previous_uuids_sql(
    *,
    meta:CollectionMeta,
):
    return f'''
        DELETE FROM {meta.change_meta.buffer_table_name}
        WHERE uuid IN (
          SELECT jt.previous_uuid
          FROM {meta.canonical_table_name},
            JSON_TABLE(json_document, '$'
              COLUMNS (
                uuid VARCHAR2(36) PATH '$.uuid',
                NESTED PATH '$.info.previousUuids[*]'
                  COLUMNS (
                    previous_uuid VARCHAR2(36) PATH '$'
                  )
              )
            )
            AS jt
            WHERE JSON_EXISTS(json_document, '$.info.previousUuids') AND jt.previous_uuid IS NOT NULL
        )
    '''

def delete_changes_matching_previous_uuids(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    sql = delete_changes_matching_previous_uuids_sql(
        meta=meta,
    )
    cursor.execute(sql)

def process_changes_matching_previous_uuids(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    connection = cursor.connection
    connection.begin()

    try:
        insert_change_history_matching_previous_uuids(
            cursor,
            meta=meta,
        )

        delete_changes_matching_previous_uuids(
            cursor,
            meta=meta,
        )
    except Exception as e:
        connection.rollback()
        raise e

    connection.commit()

def truncate_staging(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    cursor.execute(f'TRUNCATE TABLE {meta.staging_table_name}')

def distinct_change_uuids_for_collection(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    cursor.execute(
        f'SELECT DISTINCT(uuid) FROM {meta.change_meta.buffer_table_name} WHERE family_system_name = :family_system_name',
        {'family_system_name': meta.family_system_name}
    )
    return [row[0] for row in cursor.fetchall()]

def insert_change_history_matching_staging_sql(
    *,
    meta:CollectionMeta,
):
    return f'''
        MERGE INTO {meta.change_meta.history_table_name} pjh
        USING (
          SELECT
            uuid,
            pure_version,
            family_system_name,
            change_type,
            inserted
          FROM {meta.change_meta.buffer_table_name}
          WHERE uuid IN (
            SELECT uuid FROM {meta.staging_table_name}
          )
        ) pj
        ON (pj.uuid = pjh.uuid AND pj.pure_version = pjh.pure_version)
        WHEN NOT MATCHED THEN
          INSERT (pjh.uuid, pjh.pure_version, pjh.family_system_name, pjh.change_type, pjh.inserted)
          VALUES (pj.uuid, pj.pure_version, pj.family_system_name, pj.change_type, pj.inserted)
    '''

def insert_change_history_matching_staging(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    sql = insert_change_history_matching_staging_sql(
        meta=meta,
    )
    cursor.execute(sql)

def delete_changes_matching_staging_sql(
    *,
    meta:CollectionMeta,
):
    return f'''
        DELETE FROM {meta.change_meta.buffer_table_name}
        WHERE uuid IN (
          SELECT uuid FROM {meta.staging_table_name}
        )
    '''

def delete_changes_matching_staging(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    sql = delete_changes_matching_staging_sql(
        meta=meta,
    )
    cursor.execute(sql)

def process_changes_matching_staging(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    connection = cursor.connection
    connection.begin()

    try:
        insert_change_history_matching_staging(
            cursor,
            meta=meta,
        )

        delete_changes_matching_staging(
            cursor,
            meta=meta,
        )
    except Exception as e:
        connection.rollback()
        raise e

    connection.commit()

def merge_documents_from_staging_sql(
    *,
    meta:CollectionMeta,
):
    return f'''
        MERGE INTO {meta.canonical_table_name} pj
        USING (
          SELECT uuid, inserted, json_document, updated, pure_created, pure_modified FROM ( 
            SELECT uuid, inserted, json_document, updated, pure_created, pure_modified,
              RANK() OVER (PARTITION BY uuid ORDER BY pure_modified DESC) latest
              FROM {meta.staging_table_name}
          ) where latest = 1
        ) pjs
        ON (pjs.uuid = pj.uuid)
        WHEN MATCHED
          THEN UPDATE SET
            pj.pure_modified = pjs.pure_modified,
            pj.updated = pjs.updated,
            pj.json_document = pjs.json_document
          WHERE
            pjs.pure_modified > pj.pure_modified
        WHEN NOT MATCHED
          THEN INSERT (pj.uuid, pj.inserted, pj.json_document, pj.updated, pj.pure_created, pj.pure_modified)
          VALUES (pjs.uuid, pjs.inserted, pjs.json_document, pjs.updated, pjs.pure_created, pjs.pure_modified)
    '''

def merge_documents_from_staging(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    sql = merge_documents_from_staging_sql(
        meta=meta,
    )
    cursor.execute(sql)

def delete_documents_matching_previous_uuids_sql(
    *,
    meta:CollectionMeta,
):
    return f'''
        DELETE FROM {meta.canonical_table_name}
        WHERE uuid IN (
          SELECT jt.previous_uuid
          FROM {neta.canonical_table_name},
            JSON_TABLE(json_document, '$'
              COLUMNS (
                uuid VARCHAR2(36) PATH '$.uuid',
                NESTED PATH '$.info.previousUuids[*]'
                  COLUMNS (
                    previous_uuid VARCHAR2(36) PATH '$'
                  )
              )
            )
            AS jt
            WHERE JSON_EXISTS(json_document, '$.info.previousUuids') AND jt.previous_uuid IS NOT NULL
        )
    '''

def delete_documents_matching_previous_uuids(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    sql = delete_documents_matching_previous_uuids_sql(
        meta=meta,
    )
    cursor.execute(sql)

def load_documents_from_staging(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    connection = cursor.connection
    connection.begin()

    try:
        merge_documents_from_staging(
            cursor,
            meta=meta,
        )

        delete_documents_matching_previous_uuids(
            cursor,
            meta=meta,
        )

        truncate_staging(
            cursor,
            meta=meta,
        )

    except Exception as e:
        connection.rollback()
        raise e

    connection.commit()

def delete_documents_matching_uuids_sql(
    cursor:cx_Oracle.Cursor,
    *,
    uuids:list[str],
    meta:CollectionMeta,
    staging:bool=False
):
    collection_table_name = meta.staging_table_name if staging else meta.canonical_table_name
    bind_vars = ','.join(f':{i}' for i in range(len(uuids)))
    return f'''
        DELETE FROM {collection_table_name}
        WHERE uuid IN ({bind_vars})
    '''

def delete_documents_matching_uuids(
    cursor:cx_Oracle.Cursor,
    *,
    uuids:list[str],
    meta:CollectionMeta,
    staging:bool=False
):
    sql = delete_documents_matching_uuids_sql(
        cursor,
        uuids=uuids,
        meta=meta,
        staging=staging,
    )
    cursor.execute(sql, uuids)

def insert_change_history_matching_uuids_sql(
    cursor:cx_Oracle.Cursor,
    *,
    uuids:list[str],
    meta:ChangeMeta,
):
    bind_vars = ','.join(f':{i}' for i in range(len(uuids)))
    return f'''
        MERGE INTO {meta.history_table_name} pjh
        USING (
          SELECT
            uuid,
            pure_version,
            family_system_name,
            change_type,
            inserted
          FROM {meta.buffer_table_name}
          WHERE uuid in ({bind_vars})
        ) pj
        ON (pj.uuid = pjh.uuid AND pj.pure_version = pjh.pure_version)
        WHEN NOT MATCHED THEN
          INSERT (pjh.uuid, pjh.pure_version, pjh.family_system_name, pjh.change_type, pjh.inserted)
          VALUES (pj.uuid, pj.pure_version, pj.family_system_name, pj.change_type, pj.inserted)
    '''

def insert_change_history_matching_uuids(
    cursor:cx_Oracle.Cursor,
    *,
    uuids:list[str],
    meta:ChangeMeta,
):
    sql = insert_change_history_matching_uuids_sql(
        cursor,
        uuids=uuids,
        meta=meta,
    )
    cursor.execute(sql, uuids)

def delete_changes_matching_uuids_sql(
    cursor:cx_Oracle.Cursor,
    *,
    uuids:list[str],
    meta:ChangeMeta,
):
    bind_vars = ','.join(f':{i}' for i in range(len(uuids)))
    return f'''
        DELETE FROM {meta.buffer_table_name}
        WHERE uuid IN ({bind_vars})
    '''

def delete_changes_matching_uuids(
    cursor:cx_Oracle.Cursor,
    *,
    uuids:list[str],
    meta:ChangeMeta,
):
    sql = delete_changes_matching_uuids_sql(
        cursor,
        uuids=uuids,
        meta=meta,
    )
    cursor.execute(sql, uuids)

def delete_documents_and_changes_matching_uuids(
    cursor:cx_Oracle.Cursor,
    *,
    uuids:list[str],
    meta:CollectionMeta,
):
    connection = cursor.connection
    connection.begin()

    try:
        delete_documents_matching_uuids(
            cursor,
            uuids=uuids,
            meta=meta,
        )

        insert_change_history_matching_uuids(
            cursor,
            uuids=uuids,
            meta=meta.change_meta,
        )

        delete_changes_matching_uuids(
            cursor,
            uuids=uuids,
            meta=meta.change_meta,
        )
    except Exception as e:
        connection.rollback()
        raise e

    connection.commit()

def research_output_scopus_ids_since_sql(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta, # Enforce this to be research-outputs somehow?
):
    return f'''
        SELECT
          pjro.scopus_id
        FROM
          {meta.canonical_table_name} ro,
          JSON_TABLE(ro.json_document, '$'
            COLUMNS (
              scopus_id        PATH '$.externalId',
              uuid             PATH '$.uuid',
              external_source  PATH '$.externalIdSource',
              ro_title         PATH '$.title.value',
              ro_type          PATH '$.type.uri',
              NESTED PATH '$.publicationStatuses[*]'
                COLUMNS (
                  ro_year PATH '$.publicationDate.year',
                  ro_current PATH '$.current',
                  ro_status PATH '$.publicationStatus.uri'
                )
            )) pjro
        WHERE JSON_EXISTS(ro.json_document, '$.uuid')
          AND pjro.external_source = 'Scopus'
          AND pjro.ro_type LIKE '/dk/atira/pure/researchoutput/researchoutputtypes/contributiontojournal/%'
          AND pjro.ro_current = 'true'
          AND pjro.ro_status = '/dk/atira/pure/researchoutput/status/published'
          AND TO_DATE(pjro.ro_year, 'YYYY') > :published_datetime
          AND (
            ro.pure_created >= :created_modified_datetime OR
            ro.pure_modified >= :created_modified_datetime
          )
    '''

def research_output_scopus_ids_since(
    cursor:cx_Oracle.Cursor,
    *,
    published_datetime:datetime,
    created_modified_datetime:datetime,
    meta:CollectionMeta, # Enforce this to be research-outputs somehow?
):
    sql = research_output_scopus_ids_since_sql(
        cursor,
        meta=meta,
    )
    columns = [col[0] for col in cursor.description]
    cursor.rowfactory = lambda *args: dict(zip(columns, args))
    cursor.execute(
        sql,
        published_datetime=published_datetime,
        created_modified_datetime=created_modified_datetime
    )
    return cursor.fetchall()
