from datetime import datetime
import functools
import json
from typing import Any, Callable, MutableMapping, Tuple, TypeVar, cast

from experts_dw import db
from experts_dw.exceptions import ExpertsDwException

iso_8601_format = '%Y-%m-%dT%H:%M:%S.%f%z'

F = TypeVar('F', bound=Callable[..., Any])

@functools.lru_cache(maxsize=None)
def collection_local_names(cursor):
    cursor.execute(
        'SELECT DISTINCT(local_name) FROM scopus_json_collection_meta',
    )
    return [row[0] for row in cursor.fetchall()]

@functools.lru_cache(maxsize=None)
def collection_local_name_for_api_name(cursor, *, collection_api_name):
    cursor.execute(
        'SELECT local_name FROM scopus_json_collection_meta WHERE api_name = :api_name',
        {'api_name': collection_api_name}
    )
    result = cursor.fetchone()
    if result is None:
        return result
    else:
        return result[0] # Result will be a tuple

@functools.lru_cache(maxsize=None)
def collection_local_name_for_schema_record_name(cursor, *, collection_schema_record_name):
    cursor.execute(
        'SELECT local_name FROM scopus_json_collection_meta WHERE schema_record_name = :schema_record_name',
        {'schema_record_name': collection_schema_record_name}
    )
    result = cursor.fetchone()
    if result is None:
        return result
    else:
        return result[0] # Result will be a tuple

@functools.lru_cache(maxsize=None)
def collection_schema_record_name_for_local_name(cursor, *, collection_local_name):
    cursor.execute(
        'SELECT schema_record_name FROM scopus_json_collection_meta WHERE local_name = :local_name',
        {'local_name': collection_local_name}
    )
    result = cursor.fetchone()
    if result is None:
        return result
    else:
        return result[0] # Result will be a tuple

@functools.lru_cache(maxsize=None)
def collection_api_name_for_local_name(cursor, *, collection_local_name):
    cursor.execute(
        'SELECT api_name FROM scopus_json_collection_meta WHERE local_name = :local_name',
        {'local_name': collection_local_name}
    )
    result = cursor.fetchone()
    if result is None:
        return result
    else:
        return result[0] # Result will be a tuple

class MissingCollectionName(ValueError, ExpertsDwException):
    '''Raised when a Scopus collection name is expected but missing.'''
    def __init__(self, *args, **kwargs):
        super().__init__(
            'No collection_local_name, collection_api_name, or collection_schema_record_name found in kwargs',
            *args,
            **kwargs
        )

class InvalidCollectionLocalName(ValueError, ExpertsDwException):
    '''Raised when a local collection name is invalid.'''
    def __init__(self, *args, collection_local_name, **kwargs):
        super().__init__(
            f'Invalid collection_local_name "{collection_local_name}"',
            *args,
            **kwargs
        )

class InvalidCollectionApiName(ValueError, ExpertsDwException):
    '''Raised when a Scopus API collection name is invalid.'''
    def __init__(self, *args, collection_api_name, **kwargs):
        super().__init__(
            f'Invalid collection_api_name "{collection_api_name}"',
            *args,
            **kwargs
        )

class InvalidCollectionSchemaRecordName(ValueError, ExpertsDwException):
    '''Raised when a Scopus API schema record name is invalid.'''
    def __init__(self, *args, collection_schema_record_name, **kwargs):
        super().__init__(
            f'Invalid collection_schema_record_name "{collection_schema_record_name}"',
            *args,
            **kwargs
        )

def validate_collection_names(func: F) -> F:
    '''A decorator wrapper that ensures that collection_local_name,
    collection_api_name, and collection_schema_record_name all exist in kwargs, are valid,
    and consistent with each other.

    Args:
        func: The function to be wrapped.

    Return:
        The wrapped function.

    Raises:
        MissingCollectionName: If none of the various ``collectiion_*`` names is in kwargs.
        InvalidCollectionLocalName: If the ``collection_local_name`` is not found
        InvalidCollectionApiName: If the ``collection_api_name`` is not found
        InvalidCollectionSchemaRecordName: If the ``collection_schema_record_name`` is not found
    '''
    @functools.wraps(func)
    def wrapper_validate_collection_names(*args, **kwargs):
        cursor = args[0]
        if 'collection_local_name' in kwargs and kwargs['collection_local_name'] is not None:
            if kwargs['collection_local_name'] not in collection_local_names(cursor):
                raise InvalidCollectionLocalName(
                    collection_local_name=kwargs['collection_local_name']
                )
        elif 'collection_api_name' in kwargs and kwargs['collection_api_name'] is not None:
            kwargs['collection_local_name'] = collection_local_name_for_api_name(
                cursor,
                collection_api_name=kwargs['collection_api_name']
            )
            if kwargs['collection_local_name'] is None:
                raise InvalidCollectionApiName(
                    collection_api_name=kwargs['collection_api_name']
                )
        elif 'collection_schema_record_name' in kwargs and kwargs['collection_schema_record_name'] is not None:
            kwargs['collection_local_name'] = collection_local_name_for_schema_record_name(
                cursor,
                collection_schema_record_name=kwargs['collection_schema_record_name']
            )
            if kwargs['collection_local_name'] is None:
                raise InvalidCollectionSchemaRecordName(
                    collection_schema_record_name=kwargs['collection_schema_record_name']
                )
        if ('collection_local_name' not in kwargs) or (kwargs['collection_local_name'] is None):
            raise MissingCollectionName()

        kwargs['collection_schema_record_name'] = collection_schema_record_name_for_local_name(
            cursor,
            collection_local_name=kwargs['collection_local_name']
        )
        kwargs['collection_api_name'] = collection_api_name_for_local_name(
            cursor,
            collection_local_name=kwargs['collection_local_name']
        )
        return func(*args, **kwargs)
    return cast(F, wrapper_validate_collection_names)

# Notice that this function has no validation. We recommend calling it only
# from other functions in this module that do have parameter validation.
def get_collection_table_name(*, collection_local_name, staging=False):
    collection_table_name = f'scopus_json_{collection_local_name}'
    if staging:
        return collection_table_name + '_staging'
    return collection_table_name

@validate_collection_names
def document_exists(
    cursor,
    *,
    scopus_id,
    collection_local_name=None,
    collection_api_name=None,
    collection_schema_record_name=None,
    staging=False
):
    collection_table_name = get_collection_table_name(
        collection_local_name=collection_local_name,
        staging=staging
    )
    cursor.execute(
        f'SELECT count(*) FROM {collection_table_name} WHERE scopus_id = :scopus_id',
        {'scopus_id': scopus_id}
    )
    document_count = cursor.fetchone()[0] # Result will be a tuple
    if document_count > 0:
        return True
    else:
        return False

@validate_collection_names
def insert_sql(
    cursor,
    *,
    collection_local_name=None,
    collection_api_name=None,
    collection_schema_record_name=None,
    staging=False
):
    collection_table_name = get_collection_table_name(
        collection_local_name=collection_local_name,
        staging=staging
    )
    primary_key_column_names = 'scopud_id'
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

@validate_collection_names
def insert_document(
    cursor,
    *,
    document,
    collection_local_name=None,
    collection_api_name=None,
    collection_schema_record_name=None,
    staging=False
):
    sql = insert_sql(
        cursor,
        collection_local_name=collection_local_name,
        staging=staging
    )
    cursor.execute(sql, document)

@validate_collection_names
def insert_documents(
    cursor,
    *,
    documents,
    collection_local_name=None,
    collection_api_name=None,
    collection_schema_record_name=None,
    staging=False
):
    sql = insert_sql(
        cursor,
        collection_local_name=collection_local_name,
        staging=staging
    )
    cursor.executemany(sql, documents)

@validate_collection_names
def truncate_staging(
    cursor,
    *,
    collection_local_name=None,
    collection_api_name=None,
    collection_schema_record_name=None
):
    collection_staging_table_name = get_collection_table_name(
        collection_local_name=collection_local_name,
        staging=True
    )
    cursor.execute(f'TRUNCATE TABLE {collection_staging_table_name}')

@validate_collection_names
def merge_documents_from_staging_sql(
    cursor,
    *,
    collection_local_name=None,
    collection_api_name=None,
    collection_schema_record_name=None
):
    collection_table_name = get_collection_table_name(
        collection_local_name=collection_local_name
    )
    collection_staging_table_name = get_collection_table_name(
        collection_local_name=collection_local_name,
        staging=True
    )
    return f'''
        MERGE INTO {collection_table_name} sj
        USING (
          SELECT scopus_id, inserted, json_document, updated, scopus_created, scopus_modified FROM ( 
            SELECT scopus_id, inserted, json_document, updated, scopus_created, scopus_modified,
              RANK() OVER (PARTITION BY scopus_id ORDER BY scopus_modified DESC) latest
              FROM {collection_staging_table_name}
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

@validate_collection_names
def merge_documents_from_staging(
    cursor,
    *,
    collection_local_name=None,
    collection_api_name=None,
    collection_schema_record_name=None
):
    sql = merge_documents_from_staging_sql(
        cursor,
        collection_local_name=collection_local_name
    )
    cursor.execute(sql)

@validate_collection_names
def load_documents_from_staging(
    cursor,
    *,
    collection_local_name=None,
    collection_api_name=None,
    collection_schema_record_name=None
):
    connection = cursor.connection
    connection.begin()

    try:
        merge_documents_from_staging(
            cursor,
            collection_local_name=collection_local_name
        )

        truncate_staging(
            cursor,
            collection_local_name=collection_local_name
        )

    except Exception as e:
        connection.rollback()
        raise e

    connection.commit()

@validate_collection_names
def delete_documents_matching_scopus_ids_sql(
    cursor,
    *,
    scopus_ids,
    collection_local_name=None,
    collection_api_name=None,
    collection_schema_record_name=None,
):
    collection_table_name = get_collection_table_name(
        collection_local_name=collection_local_name
    )
    bind_vars = ','.join(f':{i}' for i in range(len(scopus_ids)))
    return f'''
        DELETE FROM {collection_table_name}
        WHERE scopus_id IN ({bind_vars})
    '''

@validate_collection_names
def delete_documents_matching_scopus_ids(
    cursor,
    *,
    scopus_ids,
    collection_local_name=None,
    collection_api_name=None,
    collection_schema_record_name=None
):
    sql = delete_documents_matching_scopus_ids_sql(
        cursor,
        scopus_ids=scopus_ids,
        collection_local_name=collection_local_name
    )
    cursor.execute(sql, scopus_ids)
