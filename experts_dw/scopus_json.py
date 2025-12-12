from datetime import datetime
import functools
import json
from typing import Any, Callable, Iterable, MutableMapping, Tuple, TypeVar, cast

import cx_Oracle

from experts_dw import db, pure_json_collection_meta
from experts_dw.exceptions import ExpertsDwException
from experts_dw.scopus_json_collection_meta import CollectionMeta

def document_exists(
    cursor:cx_Oracle.Cursor,
    *,
    scopus_id:str,
    meta:CollectionMeta,
    staging:bool=False
):
    collection_table_name = meta.staging_table_name if staging else meta.canonical_table_name
    cursor.execute(
        f'SELECT count(*) FROM {collection_table_name} WHERE scopus_id = :scopus_id',
        {'scopus_id': scopus_id}
    )
    document_count = cursor.fetchone()[0] # Result will be a tuple
    if document_count > 0:
        return True
    else:
        return False

def insert_sql(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
    staging:bool=False
):
    collection_table_name = meta.staging_table_name if staging else meta.canonical_table_name
    primary_key_column_names = 'scopus_id'
    primary_key_predicate = 'scopus_id = :scopus_id'
    if staging:
        primary_key_column_names = primary_key_column_names + ', scopus_modified'
        primary_key_predicate = primary_key_predicate + ' AND scopus_modified = :scopus_modified'
    return f'''
        INSERT /*+ ignore_row_on_dupkey_index({collection_table_name}({primary_key_column_names})) */ 
        INTO {collection_table_name}
        (
          scopus_id,
          scopus_created,
          scopus_modified,
          inserted,
          updated,
          json_document
        ) VALUES (
          :scopus_id,
          :scopus_created,
          :scopus_modified,
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
        cursor,
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
        cursor,
        meta=meta,
        staging=staging
    )
    cursor.executemany(sql, documents)

def delete_scopus_ids_for_downloaded_records_from_to_download_list_sql(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    return f'''
        DELETE
        FROM {meta.to_download_table_name}
        WHERE scopus_id IN (
          SELECT defunct.scopus_id
          FROM {meta.defunct_table_name} defunct
          UNION
          SELECT to_download.scopus_id
          FROM {meta.to_download_table_name} to_download
          JOIN {meta.staging_table_name} staging
          ON to_download.scopus_id = staging.scopus_id
          WHERE to_download.inserted < staging.inserted
          UNION
          SELECT to_download.scopus_id
          FROM {meta.to_download_table_name} to_download
          JOIN {meta.canonical_table_name} canonical
          ON to_download.scopus_id = canonical.scopus_id
          WHERE to_download.inserted < canonical.inserted
        )
    '''

def delete_scopus_ids_for_downloaded_records_from_to_download_list(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    sql = delete_scopus_ids_for_downloaded_records_from_to_download_list_sql(
        cursor,
        meta=meta,
    )
    cursor.execute(sql)

def truncate_staging(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    cursor.execute(f'TRUNCATE TABLE {meta.staging_table_name}')

def merge_documents_from_staging_sql(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    return f'''
        MERGE INTO {meta.canonical_table_name} canonical
        USING (
          SELECT scopus_id, inserted, json_document, updated, scopus_created, scopus_modified FROM ( 
            SELECT scopus_id, inserted, json_document, updated, scopus_created, scopus_modified,
              RANK() OVER (PARTITION BY scopus_id ORDER BY scopus_modified DESC) latest
              FROM {meta.staging_table_name}
          ) WHERE latest = 1
        ) staging
        ON (staging.scopus_id = canonical.scopus_id)
        WHEN MATCHED
          THEN UPDATE SET
            canonical.scopus_modified = staging.scopus_modified,
            canonical.updated         = staging.updated,
            canonical.json_document   = staging.json_document
          WHERE
            staging.scopus_modified > canonical.scopus_modified
        WHEN NOT MATCHED
          THEN INSERT (canonical.scopus_id, canonical.inserted, canonical.json_document, canonical.updated, canonical.scopus_created, canonical.scopus_modified)
          VALUES (staging.scopus_id, staging.inserted, staging.json_document, staging.updated, staging.scopus_created, staging.scopus_modified)
    '''

def merge_documents_from_staging(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    sql = merge_documents_from_staging_sql(
        cursor,
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

        delete_scopus_ids_for_downloaded_records_from_to_download_list(
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

def delete_documents_matching_scopus_ids_sql(
    cursor:cx_Oracle.Cursor,
    *,
    scopus_ids:list[str],
    meta:CollectionMeta,
    # Should we support this for staging tables, too?
):
    bind_vars = ','.join(f':{i}' for i in range(len(scopus_ids)))
    return f'''
        DELETE FROM {meta.canonical_table_name}
        WHERE scopus_id IN ({bind_vars})
    '''

def delete_documents_matching_scopus_ids(
    cursor:cx_Oracle.Cursor,
    *,
    scopus_ids:list[str],
    meta:CollectionMeta,
    # Should we support this for staging tables, too?
):
    sql = delete_documents_matching_scopus_ids_sql(
        cursor,
        scopus_ids=scopus_ids,
        meta=meta,
    )
    cursor.execute(sql, scopus_ids)

def insert_defunct_scopus_ids_sql(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    return f'''
        INSERT /*+ ignore_row_on_dupkey_index({meta.defunct_table_name}(scopus_id)) */
        INTO {meta.defunct_table_name}
        (
          scopus_id,
          inserted
        ) VALUES (
          :scopus_id,
          :inserted
        )
    '''

def insert_defunct_scopus_ids(
    cursor:cx_Oracle.Cursor,
    *,
    scopus_ids:Iterable[str],
    meta:CollectionMeta,
):
    cursor.executemany(
        insert_defunct_scopus_ids_sql(
            cursor,
            meta=meta,
        ),
        [
            {
                'scopus_id': scopus_id,
                'inserted': datetime.now(),
            }
            for scopus_id in scopus_ids
        ],
    )

def insert_scopus_ids_to_download_sql(
    cursor:cx_Oracle.Cursor,
    *,
    meta:CollectionMeta,
):
    return f'''
        INSERT /*+ ignore_row_on_dupkey_index({meta.to_download_table_name}(scopus_id)) */
        INTO {meta.to_download_table_name}
        (
          scopus_id,
          inserted
        ) VALUES (
          :scopus_id,
          :inserted
        )
    '''

def insert_scopus_ids_to_download(
    cursor:cx_Oracle.Cursor,
    *,
    scopus_ids:Iterable[str],
    meta:CollectionMeta,
):
    cursor.executemany(
        insert_scopus_ids_to_download_sql(
            cursor,
            meta=meta,
        ),
        [
            {
                'scopus_id': scopus_id,
                'inserted': datetime.now(),
            }
            for scopus_id in scopus_ids
        ],
    )

def update_abstract_to_download_sql(
    cursor:cx_Oracle.Cursor,
    *,
    # Maybe create something like the following, to make the types more specific?
    #abstract_meta:AbstractCollectionMeta,
    abstract_meta:CollectionMeta,
    citation_meta:CollectionMeta,
    pure_ro_meta:pure_json_collection_meta.CollectionMeta,
    past_months_limit:int=36, # Past 36 months, 3 years is our default reporting window
):
    return f'''
        MERGE INTO {abstract_meta.to_download_table_name} to_download
        USING (
          WITH scopus_id_to_exclude AS (
            SELECT scopus_id FROM {abstract_meta.defunct_table_name}
            UNION
            SELECT scopus_id FROM {citation_meta.defunct_table_name}
          )
          SELECT
            rojt.scopus_id
          FROM
            -- pure json research output:
            {pure_ro_meta.canonical_table_name} ro,
            JSON_TABLE(ro.json_document, '$'
              COLUMNS (
                scopus_id       PATH '$.externalId',
                external_source PATH '$.externalIdSource',
                ro_type         PATH '$.type.uri',
                NESTED PATH '$.publicationStatuses[*]'
                  COLUMNS (
                    ro_year    PATH '$.publicationDate.year',
                    ro_current PATH '$.current',
                    ro_status  PATH '$.publicationStatus.uri'
                  )
              )) rojt
          LEFT JOIN scopus_id_to_exclude exclude
            ON rojt.scopus_id = exclude.scopus_id
          WHERE exclude.scopus_id IS NULL
            AND rojt.external_source = 'Scopus'
            AND rojt.ro_type LIKE '/dk/atira/pure/researchoutput/researchoutputtypes/contributiontojournal/%'
            AND rojt.ro_current = 'true'
            AND rojt.ro_status = '/dk/atira/pure/researchoutput/status/published'
            AND TO_DATE(rojt.ro_year, 'YYYY') >= ADD_MONTHS(SYSDATE, - {past_months_limit})
            AND (
              -- This includes all the new and modified articles...
              ro.pure_modified >= (SELECT MAX(scopus_modified) FROM {abstract_meta.canonical_table_name})
              OR
              -- ...while this includes any older articles missing from scopus_json_abstract:
              rojt.scopus_id NOT IN (SELECT scopus_id FROM {abstract_meta.canonical_table_name})
            )
        ) pure_ro
        ON (pure_ro.scopus_id = to_download.scopus_id)
        WHEN NOT MATCHED THEN
          INSERT (to_download.scopus_id, to_download.inserted)
          VALUES (pure_ro.scopus_id, SYSDATE)
    '''

def update_abstract_to_download(
    cursor:cx_Oracle.Cursor,
    *,
    abstract_meta:CollectionMeta,
    citation_meta:CollectionMeta,
    pure_ro_meta:pure_json_collection_meta.CollectionMeta,
    past_months_limit:int=36, # Past 36 months, 3 years is our default reporting window
):
    sql = update_abstract_to_download_sql(
        cursor,
        abstract_meta=abstract_meta,
        citation_meta=citation_meta,
        pure_ro_meta=pure_ro_meta,
        past_months_limit=past_months_limit,
    )
    cursor.execute(sql)
