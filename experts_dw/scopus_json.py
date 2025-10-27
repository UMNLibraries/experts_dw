from datetime import datetime
import functools
import json
from typing import Any, Callable, MutableMapping, Tuple, TypeVar, cast

import cx_Oracle

from experts_dw import db
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
        MERGE INTO {meta.canonical_table_name} sj
        USING (
          SELECT scopus_id, inserted, json_document, updated, scopus_created, scopus_modified FROM ( 
            SELECT scopus_id, inserted, json_document, updated, scopus_created, scopus_modified,
              RANK() OVER (PARTITION BY scopus_id ORDER BY scopus_modified DESC) latest
              FROM {meta.staging_table_name}
          ) where latest = 1
        ) sjs
        ON (sjs.scopus_id = sj.scopus_id)
        WHEN MATCHED
          THEN UPDATE SET
            sj.scopus_modified = sjs.scopus_modified,
            sj.updated = sjs.updated,
            sj.json_document = sjs.json_document
          WHERE
            sjs.scopus_modified > sj.scopus_modified
        WHEN NOT MATCHED
          THEN INSERT (sj.scopus_id, sj.inserted, sj.json_document, sj.updated, sj.scopus_created, sj.scopus_modified)
          VALUES (sjs.scopus_id, sjs.inserted, sjs.json_document, sjs.updated, sjs.scopus_created, sjs.scopus_modified)
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
        INSERT /*+ ignore_row_on_dupkey_index(scopus_{meta.local_name}_defunct(scopus_id)) */
        INTO scopus_{meta.local_name}_defunct
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
