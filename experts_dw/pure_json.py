from datetime import datetime
import functools
import json
from typing import Any, Callable, MutableMapping, Tuple, TypeVar, cast

from experts_dw import db
from experts_dw.exceptions import ExpertsDwException

iso_8601_format = '%Y-%m-%dT%H:%M:%S.%f%z'

@functools.lru_cache(maxsize=None)
def api_versions(cursor):
    cursor.execute('SELECT DISTINCT(api_version) FROM pure_json_collection_meta')
    return [row[0] for row in cursor.fetchall()]

class MissingApiVersion(ValueError, ExpertsDwException):
    '''Raised when a Pure API version is expected but missing.'''
    def __init__(self, *args, **kwargs):
        super().__init__(f'No api_version found in kwargs', *args, **kwargs)

class InvalidApiVersion(ValueError, ExpertsDwException):
    '''Raised when a Pure API version is unrecognized.'''
    def __init__(self, api_version, *args, **kwargs):
        super().__init__(f'Invalid api_version "{api_version}"', *args, **kwargs)

F = TypeVar('F', bound=Callable[..., Any])

def validate_api_version(func: F) -> F:
    '''A decorator wrapper that validates a kwarg Pure API version.

    Args:
        func: The function to be wrapped.

    Return:
        The wrapped function.

    Raises:
        MissingApiVersion: If the ``api_version`` kwarg is missing or
            the value is None.
        InvalidApiVersion: If the ``api_version`` is unrecognized.
    '''
    @functools.wraps(func)
    def wrapper_validate_api_version(*args, **kwargs):
        cursor = args[0]
        if 'api_version' in kwargs and kwargs['api_version'] is not None:
            if kwargs['api_version'] not in api_versions(cursor):
                raise InvalidApiVersion(kwargs['api_version'])
        if ('api_version' not in kwargs) or (kwargs['api_version'] is None):
            raise MissingApiVersion()
        return func(*args, **kwargs)
    return cast(F, wrapper_validate_api_version)

@functools.lru_cache(maxsize=None)
@validate_api_version
def collection_local_names_for_api_version(cursor, *, api_version):
    cursor.execute(
        'SELECT DISTINCT(local_name) FROM pure_json_collection_meta where api_version = :api_version',
        {'api_version': api_version}
    )
    return [row[0] for row in cursor.fetchall()]

@functools.lru_cache(maxsize=None)
@validate_api_version
def collection_family_system_names_for_api_version(cursor, *, api_version):
    cursor.execute(
        'SELECT DISTINCT(family_system_name) FROM pure_json_collection_meta where api_version = :api_version',
        {'api_version': api_version}
    )
    return [row[0] for row in cursor.fetchall()]

@functools.lru_cache(maxsize=None)
@validate_api_version
def collection_api_names_for_api_version(cursor, *, api_version):
    cursor.execute(
        'SELECT DISTINCT(api_name) FROM pure_json_collection_meta where api_version = :api_version',
        {'api_version': api_version}
    )
    return [row[0] for row in cursor.fetchall()]

@functools.lru_cache(maxsize=None)
@validate_api_version
def collection_local_name_for_api_name(cursor, *, collection_api_name, api_version):
    cursor.execute(
        'SELECT local_name FROM pure_json_collection_meta WHERE api_name = :api_name AND api_version = :api_version',
        {'api_name': collection_api_name, 'api_version': api_version}
    )
    result = cursor.fetchone()
    if result is None:
        return result
    else:
        return result[0] # Result will be a tuple

@functools.lru_cache(maxsize=None)
@validate_api_version
def collection_local_name_for_family_system_name(cursor, *, collection_family_system_name, api_version):
    cursor.execute(
        'SELECT local_name FROM pure_json_collection_meta WHERE family_system_name = :family_system_name AND api_version = :api_version',
        {'family_system_name': collection_family_system_name, 'api_version': api_version}
    )
    result = cursor.fetchone()
    if result is None:
        return result
    else:
        return result[0] # Result will be a tuple

@functools.lru_cache(maxsize=None)
@validate_api_version
def collection_family_system_name_for_local_name(cursor, *, collection_local_name, api_version):
    cursor.execute(
        'SELECT family_system_name FROM pure_json_collection_meta WHERE local_name = :local_name AND api_version = :api_version',
        {'local_name': collection_local_name, 'api_version': api_version}
    )
    result = cursor.fetchone()
    if result is None:
        return result
    else:
        return result[0] # Result will be a tuple

@functools.lru_cache(maxsize=None)
@validate_api_version
def collection_api_name_for_local_name(cursor, *, collection_local_name, api_version):
    cursor.execute(
        'SELECT api_name FROM pure_json_collection_meta WHERE local_name = :local_name AND api_version = :api_version',
        {'local_name': collection_local_name, 'api_version': api_version}
    )
    result = cursor.fetchone()
    if result is None:
        return result
    else:
        return result[0] # Result will be a tuple

class MissingCollectionName(ValueError, ExpertsDwException):
    '''Raised when a Pure collection name is expected but missing.'''
    def __init__(self, *args, **kwargs):
        super().__init__(
            'No collection_local_name, collection_api_name, or collection_family_system_name found in kwargs',
            *args,
            **kwargs
        )

class InvalidCollectionLocalName(ValueError, ExpertsDwException):
    '''Raised when a local collection name is invalid for a given Pure API version.'''
    def __init__(self, *args, collection_local_name, api_version, **kwargs):
        super().__init__(
            f'Invalid collection_local_name "{collection_local_name}" for api_version "{api_version}"',
            *args,
            **kwargs
        )

class InvalidCollectionApiName(ValueError, ExpertsDwException):
    '''Raised when an Pure API collection name is invalid for a given API version.'''
    def __init__(self, *args, collection_api_name, api_version, **kwargs):
        super().__init__(
            f'Invalid collection_api_name "{collection_api_name}" for api_version "{api_version}"',
            *args,
            **kwargs
        )

class InvalidCollectionFamilySystemName(ValueError, ExpertsDwException):
    '''Raised when an Pure API family system name is invalid for a given API version.'''
    def __init__(self, *args, collection_family_system_name, api_version, **kwargs):
        super().__init__(
            f'Invalid collection_family_system_name "{collection_family_system_name}" for api_version "{api_version}"',
            *args,
            **kwargs
        )

def validate_collection_names(func: F) -> F:
    '''A decorator wrapper that ensures that collection_local_name,
    collection_api_name, and collection_system_name all exist in kwargs, are valid,
    and consistent with each other.

    Args:
        func: The function to be wrapped.

    Return:
        The wrapped function.

    Raises:
        MissingCollectionName: If none of the various ``collectiion_*`` names
            is in kwargs.
        InvalidCollectionLocalName: If the ``collection_local_name`` is not
            found for the given ``api_version``.
        InvalidCollectionApiName: If the ``collection_api_name`` is not found
            for the given ``api_version``.
        InvalidCollectionFamilySystemName: If the ``collection_family_system_name``
            is not found for the given ``api_version``.
    '''
    @functools.wraps(func)
    def wrapper_validate_collection_names(*args, **kwargs):
        cursor = args[0]
        api_version = kwargs['api_version']
        if 'collection_local_name' in kwargs and kwargs['collection_local_name'] is not None:
            if kwargs['collection_local_name'] not in collection_local_names_for_api_version(cursor, api_version=api_version):
                raise InvalidCollectionLocalName(
                    collection_local_name=kwargs['collection_local_name'],
                    api_version=api_version
                )
        elif 'collection_api_name' in kwargs and kwargs['collection_api_name'] is not None:
            kwargs['collection_local_name'] = collection_local_name_for_api_name(
                cursor,
                collection_api_name=kwargs['collection_api_name'],
                api_version=api_version
            )
            if kwargs['collection_local_name'] is None:
                raise InvalidCollectionApiName(
                    collection_api_name=kwargs['collection_api_name'],
                    api_version=api_version
                )
        elif 'collection_family_system_name' in kwargs and kwargs['collection_family_system_name'] is not None:
            kwargs['collection_local_name'] = collection_local_name_for_family_system_name(
                cursor,
                collection_family_system_name=kwargs['collection_family_system_name'],
                api_version=api_version
            )
            if kwargs['collection_local_name'] is None:
                raise InvalidCollectionFamilySystemName(
                    collection_family_system_name=kwargs['collection_family_system_name'],
                    api_version=api_version
                )
        if ('collection_local_name' not in kwargs) or (kwargs['collection_local_name'] is None):
            raise MissingCollectionName()
        kwargs['collection_family_system_name'] = collection_family_system_name_for_local_name(
            cursor,
            collection_local_name=kwargs['collection_local_name'],
            api_version=api_version
        )
        kwargs['collection_api_name'] = collection_api_name_for_local_name(
            cursor,
            collection_local_name=kwargs['collection_local_name'],
            api_version=api_version
        )
        return func(*args, **kwargs)
    return cast(F, wrapper_validate_collection_names)

# Notice that this function has no validation. We recommend calling it only
# from other functions in this module that do have parameter validation.
def get_change_table_name(*, api_version, history=False):
    change_table_name = f'pure_json_change_{api_version}'
    if history:
        return change_table_name + '_history'
    return change_table_name

# Notice that this function has no validation. We recommend calling it only
# from other functions in this module that do have parameter validation.
def get_collection_table_name(*, api_version, collection_local_name, staging=False):
    collection_table_name = f'pure_json_{collection_local_name}_{api_version}'
    if staging:
        return collection_table_name + '_staging'
    return collection_table_name

@validate_api_version
@validate_collection_names
def document_exists(
    cursor,
    *,
    uuid,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None,
    staging=False
):
    collection_table_name = get_collection_table_name(
        api_version=api_version,
        collection_local_name=collection_local_name,
        staging=staging
    )
    cursor.execute(
        f'SELECT count(*) FROM {collection_table_name} WHERE uuid = :uuid',
        {'uuid': uuid}
    )
    document_count = cursor.fetchone()[0] # Result will be a tuple
    if document_count > 0:
        return True
    else:
        return False

@validate_api_version
@validate_collection_names
def insert_sql(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None,
    staging=False
):
    collection_table_name = get_collection_table_name(
        api_version=api_version,
        collection_local_name=collection_local_name,
        staging=staging
    )
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
        WHERE NOT EXISTS (
          SELECT * FROM {collection_table_name}
          WHERE {primary_key_predicate}
        )
    '''

@validate_api_version
@validate_collection_names
def insert_document(
    cursor,
    *,
    document,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None,
    staging=False
):
    sql = insert_sql(
        cursor,
        collection_local_name=collection_local_name,
        api_version=api_version,
        staging=staging
    )
    cursor.execute(sql, document)

@validate_api_version
@validate_collection_names
def insert_documents(
    cursor,
    *,
    documents,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None,
    staging=False
):
    sql = insert_sql(
        cursor,
        collection_local_name=collection_local_name,
        api_version=api_version,
        staging=staging
    )
    cursor.executemany(sql, documents)

@validate_api_version
def max_change_history_inserted_date(
    cursor,
    *,
    api_version
):
    change_history_table_name = get_change_table_name(
        api_version=api_version,
        history=True
    )
    cursor.execute(
        f'SELECT MAX(inserted) FROM {change_history_table_name}'
    )
    return cursor.fetchone()[0] # Result will be a tuple

@validate_api_version
def max_change_inserted_date(
    cursor,
    *,
    api_version
):
    change_table_name = get_change_table_name(
        api_version=api_version
    )
    cursor.execute(
        f'SELECT MAX(inserted) FROM {change_table_name}'
    )
    return cursor.fetchone()[0] # Result will be a tuple

@validate_api_version
def max_pure_version_for_change_history_uuid(
    cursor,
    *,
    uuid,
    api_version
):
    change_history_table_name = get_change_table_name(
        api_version=api_version,
        history=True
    )
    cursor.execute(
        f'SELECT MAX(pure_version) FROM {change_history_table_name} WHERE uuid = :uuid',
        {'uuid': uuid}
    )
    return cursor.fetchone()[0] # Result will be a tuple

@validate_api_version
def max_pure_version_for_change_uuid(
    cursor,
    *,
    uuid,
    api_version
):
    change_table_name = get_change_table_name(
        api_version=api_version
    )
    cursor.execute(
        f'SELECT MAX(pure_version) FROM {change_table_name} WHERE uuid = :uuid',
        {'uuid': uuid}
    )
    return cursor.fetchone()[0] # Result will be a tuple

@validate_api_version
def change_document_exists(
    cursor,
    *,
    uuid,
    pure_version,
    api_version
):
    change_table_name = get_change_table_name(
        api_version=api_version
    )
    cursor.execute(
        f'SELECT count(*) FROM {change_table_name} WHERE uuid = :uuid AND pure_version = :pure_version',
        {'uuid': uuid, 'pure_version': pure_version}
    )
    document_count = cursor.fetchone()[0] # Result will be a tuple
    if document_count > 0:
        return True
    else:
        return False

@validate_api_version
def change_history_exists(
    cursor,
    *,
    uuid,
    pure_version,
    api_version
):
    change_history_table_name = get_change_table_name(
        api_version=api_version,
        history=True
    )
    cursor.execute(
        f'SELECT count(*) FROM {change_history_table_name} WHERE uuid = :uuid AND pure_version = :pure_version',
        {'uuid': uuid, 'pure_version': pure_version}
    )
    history_count = cursor.fetchone()[0] # Result will be a tuple
    if history_count > 0:
        return True
    else:
        return False

@validate_api_version
def insert_change_sql(
    cursor,
    *,
    api_version
):
    change_table_name = get_change_table_name(
        api_version=api_version
    )
    return f'''
        INSERT /*+ ignore_row_on_dupkey_index({change_table_name}(uuid, pure_version)) */ 
        INTO {change_table_name}
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
        WHERE NOT EXISTS (
          SELECT * FROM {change_table_name}
          WHERE uuid = :uuid AND pure_version = :pure_version
        )
    '''

@validate_api_version
def insert_change_documents(
    cursor,
    *,
    documents,
    api_version
):
    sql = insert_change_sql(
        cursor,
        api_version=api_version
    )
    cursor.executemany(sql, documents)

@validate_api_version
@validate_collection_names
def delete_documents_based_on_changes_sql(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None,
    staging=False
):
    # Not bothering to check for max(pure_version) here because historically
    # DELETEs have always been the max version.
    collection_table_name = get_collection_table_name(
        api_version=api_version,
        collection_local_name=collection_local_name
    )
    change_table_name = get_change_table_name(
        api_version=api_version
    )
    return f'''
        DELETE FROM {collection_table_name}
        WHERE uuid IN (
          SELECT uuid FROM {change_table_name}
          WHERE change_type = 'DELETE'
          AND family_system_name = '{collection_family_system_name}'
        )
    '''

@validate_api_version
@validate_collection_names
def delete_documents_based_on_changes(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None,
    staging=False
):
    sql = delete_documents_based_on_changes_sql(
        cursor,
        collection_local_name=collection_local_name,
        api_version=api_version
    )
    cursor.execute(sql)

@validate_api_version
@validate_collection_names
def insert_change_deletes_history_sql(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None,
    staging=False
):
    change_table_name = get_change_table_name(
        api_version=api_version
    )
    change_history_table_name = get_change_table_name(
        api_version=api_version,
        history=True
    )
    return f'''
        INSERT /*+ ignore_row_on_dupkey_index({change_history_table_name}(uuid, pure_version)) */ 
        INTO {change_history_table_name} pjh
        (
          pjh.uuid,
          pjh.pure_version,
          pjh.family_system_name,
          pjh.change_type,
          pjh.inserted
        )
        SELECT
          pj.uuid,
          pj.pure_version,
          pj.family_system_name,
          pj.change_type,
          pj.inserted
        FROM {change_table_name} pj
        WHERE 
          pj.change_type = 'DELETE'
          AND pj.family_system_name = '{collection_family_system_name}'
          AND NOT EXISTS (
            SELECT * FROM {change_history_table_name} pjh2
            WHERE pjh2.uuid = pj.uuid
            AND pjh2.pure_version = pj.pure_version
          )
    '''

@validate_api_version
@validate_collection_names
def insert_change_deletes_history(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None,
    staging=False
):
    sql = insert_change_deletes_history_sql(
        cursor,
        collection_local_name=collection_local_name,
        api_version=api_version
    )
    cursor.execute(sql)

@validate_api_version
@validate_collection_names
def delete_change_deletes_sql(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    change_table_name = get_change_table_name(
        api_version=api_version
    )
    return f'''
        DELETE FROM {change_table_name}
        WHERE change_type = 'DELETE'
        AND family_system_name = '{collection_family_system_name}'
    '''

@validate_api_version
@validate_collection_names
def delete_change_deletes(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None,
    staging=False
):
    sql = delete_change_deletes_sql(
        cursor,
        collection_local_name=collection_local_name,
        api_version=api_version
    )
    cursor.execute(sql)

@validate_api_version
@validate_collection_names
def process_change_deletes(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    connection = cursor.connection
    connection.begin()

    try:
        delete_documents_based_on_changes(
            cursor,
            collection_local_name=collection_local_name,
            api_version=api_version
        )

        insert_change_deletes_history(
            cursor,
            collection_family_system_name=collection_family_system_name,
            api_version=api_version
        )

        delete_change_deletes(
            cursor,
            collection_family_system_name=collection_family_system_name,
            api_version=api_version
        )
    except Exception as e:
        connection.rollback()
        raise e

    connection.commit()

@validate_api_version
@validate_collection_names
def insert_change_history_matching_previous_uuids_sql(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    change_table_name = get_change_table_name(
        api_version=api_version
    )
    change_history_table_name = get_change_table_name(
        api_version=api_version,
        history=True
    )
    collection_table_name = get_collection_table_name(
        api_version=api_version,
        collection_local_name=collection_local_name
    )
    return f'''
        INSERT /*+ ignore_row_on_dupkey_index({change_history_table_name}(uuid, pure_version)) */ 
        INTO {change_history_table_name} pjh
        (
          pjh.uuid,
          pjh.pure_version,
          pjh.family_system_name,
          pjh.change_type,
          pjh.inserted
        )
        SELECT
          pj.uuid,
          pj.pure_version,
          pj.family_system_name,
          pj.change_type,
          pj.inserted
        FROM {change_table_name} pj
        WHERE pj.uuid IN (
          SELECT jt.previous_uuid
          FROM {collection_table_name},
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
        ) AND NOT EXISTS (
          SELECT * FROM {change_history_table_name} pjh2
          WHERE pjh2.uuid = pj.uuid
          AND pjh2.pure_version = pj.pure_version
        )
    '''

@validate_api_version
@validate_collection_names
def insert_change_history_matching_previous_uuids(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    sql = insert_change_history_matching_previous_uuids_sql(
        cursor,
        collection_local_name=collection_local_name,
        api_version=api_version
    )
    cursor.execute(sql)

@validate_api_version
@validate_collection_names
def delete_changes_matching_previous_uuids_sql(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    change_table_name = get_change_table_name(
        api_version=api_version
    )
    collection_table_name = get_collection_table_name(
        api_version=api_version,
        collection_local_name=collection_local_name
    )
    return f'''
        DELETE FROM {change_table_name}
        WHERE uuid IN (
          SELECT jt.previous_uuid
          FROM {collection_table_name},
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

@validate_api_version
@validate_collection_names
def delete_changes_matching_previous_uuids(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    sql = delete_changes_matching_previous_uuids_sql(
        cursor,
        collection_local_name=collection_local_name,
        api_version=api_version
    )
    cursor.execute(sql)

@validate_api_version
@validate_collection_names
def process_changes_matching_previous_uuids(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    connection = cursor.connection
    connection.begin()

    try:
        insert_change_history_matching_previous_uuids(
            cursor,
            collection_local_name=collection_local_name,
            api_version=api_version
        )

        delete_changes_matching_previous_uuids(
            cursor,
            collection_local_name=collection_local_name,
            api_version=api_version
        )
    except Exception as e:
        connection.rollback()
        raise e

    connection.commit()

@validate_api_version
@validate_collection_names
def truncate_staging(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    collection_staging_table_name = get_collection_table_name(
        api_version=api_version,
        collection_local_name=collection_local_name,
        staging=True
    )
    cursor.execute(f'TRUNCATE TABLE {collection_staging_table_name}')

@validate_api_version
@validate_collection_names
def distinct_change_uuids_for_collection(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    change_table_name = get_change_table_name(
        api_version=api_version
    )
    cursor.execute(
        f'SELECT DISTINCT(uuid) FROM {change_table_name} WHERE family_system_name = :family_system_name',
        {'family_system_name': collection_family_system_name}
    )
    return [row[0] for row in cursor.fetchall()]

@validate_api_version
@validate_collection_names
def insert_change_history_matching_staging_sql(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    change_table_name = get_change_table_name(
        api_version=api_version
    )
    change_history_table_name = get_change_table_name(
        api_version=api_version,
        history=True
    )
    collection_staging_table_name = get_collection_table_name(
        api_version=api_version,
        collection_local_name=collection_local_name,
        staging=True
    )
    return f'''
        INSERT /*+ ignore_row_on_dupkey_index({change_history_table_name}(uuid, pure_version)) */ 
        INTO {change_history_table_name} pjh
        (
          pjh.uuid,
          pjh.pure_version,
          pjh.family_system_name,
          pjh.change_type,
          pjh.inserted
        )
        SELECT
          pj.uuid,
          pj.pure_version,
          pj.family_system_name,
          pj.change_type,
          pj.inserted
        FROM {change_table_name} pj
        WHERE pj.uuid in (
          SELECT uuid FROM {collection_staging_table_name}
        ) AND NOT EXISTS (
          SELECT * FROM {change_history_table_name} pjh2
          WHERE pjh2.uuid = pj.uuid
          AND pjh2.pure_version = pj.pure_version
        )
    '''

@validate_api_version
@validate_collection_names
def insert_change_history_matching_staging(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    sql = insert_change_history_matching_staging_sql(
        cursor,
        collection_local_name=collection_local_name,
        api_version=api_version
    )
    cursor.execute(sql)

@validate_api_version
@validate_collection_names
def delete_changes_matching_staging_sql(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    change_table_name = get_change_table_name(
        api_version=api_version
    )
    collection_staging_table_name = get_collection_table_name(
        api_version=api_version,
        collection_local_name=collection_local_name,
        staging=True
    )
    return f'''
        DELETE FROM {change_table_name}
        WHERE uuid IN (
          SELECT uuid FROM {collection_staging_table_name}
        )
    '''

@validate_api_version
@validate_collection_names
def delete_changes_matching_staging(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    sql = delete_changes_matching_staging_sql(
        cursor,
        collection_local_name=collection_local_name,
        api_version=api_version
    )
    cursor.execute(sql)

@validate_api_version
@validate_collection_names
def process_changes_matching_staging(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    connection = cursor.connection
    connection.begin()

    try:
        insert_change_history_matching_staging(
            cursor,
            collection_local_name=collection_local_name,
            api_version=api_version
        )

        delete_changes_matching_staging(
            cursor,
            collection_local_name=collection_local_name,
            api_version=api_version
        )
    except Exception as e:
        connection.rollback()
        raise e

    connection.commit()

@validate_api_version
@validate_collection_names
def merge_documents_from_staging_sql(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    collection_table_name = get_collection_table_name(
        api_version=api_version,
        collection_local_name=collection_local_name
    )
    collection_staging_table_name = get_collection_table_name(
        api_version=api_version,
        collection_local_name=collection_local_name,
        staging=True
    )
    return f'''
        MERGE INTO {collection_table_name} pj
        USING (
          SELECT uuid, inserted, json_document, updated, pure_created, pure_modified FROM ( 
            SELECT uuid, inserted, json_document, updated, pure_created, pure_modified,
              RANK() OVER (PARTITION BY uuid ORDER BY pure_modified DESC) latest
              FROM {collection_staging_table_name}
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

@validate_api_version
@validate_collection_names
def merge_documents_from_staging(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    sql = merge_documents_from_staging_sql(
        cursor,
        collection_local_name=collection_local_name,
        api_version=api_version
    )
    cursor.execute(sql)

@validate_api_version
@validate_collection_names
def delete_documents_matching_previous_uuids_sql(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    collection_table_name = get_collection_table_name(
        api_version=api_version,
        collection_local_name=collection_local_name
    )
    return f'''
        DELETE FROM {collection_table_name}
        WHERE uuid IN (
          SELECT jt.previous_uuid
          FROM {collection_table_name},
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

@validate_api_version
@validate_collection_names
def delete_documents_matching_previous_uuids(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    sql = delete_documents_matching_previous_uuids_sql(
        cursor,
        collection_local_name=collection_local_name,
        api_version=api_version
    )
    cursor.execute(sql)

@validate_api_version
@validate_collection_names
def load_documents_from_staging(
    cursor,
    *,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    connection = cursor.connection
    connection.begin()

    try:
        merge_documents_from_staging(
            cursor,
            collection_local_name=collection_local_name,
            api_version=api_version
        )

        delete_documents_matching_previous_uuids(
            cursor,
            collection_local_name=collection_local_name,
            api_version=api_version
        )

        truncate_staging(
            cursor,
            collection_local_name=collection_local_name,
            api_version=api_version
        )

    except Exception as e:
        connection.rollback()
        raise e

    connection.commit()

@validate_api_version
@validate_collection_names
def delete_documents_matching_uuids_sql(
    cursor,
    *,
    uuids,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None,
    staging=False
):
    collection_table_name = get_collection_table_name(
        api_version=api_version,
        collection_local_name=collection_local_name
    )
    bind_vars = ','.join(f':{i}' for i in range(len(uuids)))
    return f'''
        DELETE FROM {collection_table_name}
        WHERE uuid IN ({bind_vars})
    '''

@validate_api_version
@validate_collection_names
def delete_documents_matching_uuids(
    cursor,
    *,
    uuids,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    sql = delete_documents_matching_uuids_sql(
        cursor,
        uuids=uuids,
        collection_local_name=collection_local_name,
        api_version=api_version
    )
    cursor.execute(sql, uuids)

@validate_api_version
@validate_collection_names
def insert_change_history_matching_uuids_sql(
    cursor,
    *,
    uuids,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    change_table_name = get_change_table_name(
        api_version=api_version
    )
    change_history_table_name = get_change_table_name(
        api_version=api_version,
        history=True
    )
    bind_vars = ','.join(f':{i}' for i in range(len(uuids)))
    return f'''
        INSERT /*+ ignore_row_on_dupkey_index({change_history_table_name}(uuid, pure_version)) */ 
        INTO {change_history_table_name} pjh
        (
          pjh.uuid,
          pjh.pure_version,
          pjh.family_system_name,
          pjh.change_type,
          pjh.inserted
        )
        SELECT
          pj.uuid,
          pj.pure_version,
          pj.family_system_name,
          pj.change_type,
          pj.inserted
        FROM {change_table_name} pj
        WHERE pj.uuid in ({bind_vars})
        AND NOT EXISTS (
          SELECT * FROM {change_history_table_name} pjh2
          WHERE pjh2.uuid = pj.uuid
          AND pjh2.pure_version = pj.pure_version
        )
    '''

@validate_api_version
@validate_collection_names
def insert_change_history_matching_uuids(
    cursor,
    *,
    uuids,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    sql = insert_change_history_matching_uuids_sql(
        cursor,
        uuids=uuids,
        collection_local_name=collection_local_name,
        api_version=api_version
    )
    cursor.execute(sql, uuids)

@validate_api_version
@validate_collection_names
def delete_changes_matching_uuids_sql(
    cursor,
    *,
    uuids,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    change_table_name = get_change_table_name(
        api_version=api_version
    )
    bind_vars = ','.join(f':{i}' for i in range(len(uuids)))
    return f'''
        DELETE FROM {change_table_name}
        WHERE uuid IN ({bind_vars})
    '''

@validate_api_version
@validate_collection_names
def delete_changes_matching_uuids(
    cursor,
    *,
    uuids,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    sql = delete_changes_matching_uuids_sql(
        cursor,
        uuids=uuids,
        collection_local_name=collection_local_name,
        api_version=api_version
    )
    cursor.execute(sql, uuids)

@validate_api_version
@validate_collection_names
def delete_documents_and_changes_matching_uuids(
    cursor,
    *,
    uuids,
    api_version,
    collection_local_name=None,
    collection_api_name=None,
    collection_family_system_name=None
):
    connection = cursor.connection
    connection.begin()

    try:
        delete_documents_matching_uuids(
            cursor,
            uuids=uuids,
            collection_local_name=collection_local_name,
            api_version=api_version
        )

        insert_change_history_matching_uuids(
            cursor,
            uuids=uuids,
            collection_local_name=collection_local_name,
            api_version=api_version
        )

        delete_changes_matching_uuids(
            cursor,
            uuids=uuids,
            collection_local_name=collection_local_name,
            api_version=api_version
        )
    except Exception as e:
        connection.rollback()
        raise e

    connection.commit()
