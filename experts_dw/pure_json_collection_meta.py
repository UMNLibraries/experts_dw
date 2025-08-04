import functools

import attrs
from attrs import field, frozen, validators

import cx_Oracle

from experts_dw import db
from experts_dw.cx_oracle_helpers import \
    select_list_of_dicts, \
    select_unique_essential_dict, \
    select_list_of_scalars, \
    NonexistentUniqueEssentialResult, \
    MultipleUniqueEssentialResults
from experts_dw.exceptions import ExpertsDwException

@functools.lru_cache(maxsize=None)
def api_versions(cursor:cx_Oracle.Cursor):
    return select_list_of_scalars(
        cursor,
        'SELECT DISTINCT(api_version) FROM pure_json_collection_meta',
    )

class InvalidApiVersion(ValueError, ExpertsDwException):
    '''Raised when a Pure API version is unrecognized.'''
    def __init__(self, api_version, *args, **kwargs):
        super().__init__(f'Invalid api_version "{api_version}"', *args, **kwargs)

class InvalidCollectionLocalName(ValueError, ExpertsDwException):
    '''Raised when a local collection name is invalid for a given Pure API version.'''
    def __init__(self, *args, local_name, api_version, **kwargs):
        super().__init__(
            f'Invalid collection local_name "{local_name}" for api_version "{api_version}"',
            *args,
            **kwargs
        )

class InvalidCollectionApiName(ValueError, ExpertsDwException):
    '''Raised when a Pure API collection name is invalid for a given Pure API version.'''
    def __init__(self, *args, api_name, api_version, **kwargs):
        super().__init__(
            f'Invalid collection api_name "{api_name}" for api_version "{api_version}"',
            *args,
            **kwargs
        )

class InvalidCollectionFamilySystemName(ValueError, ExpertsDwException):
    '''Raised when a Pure API family system name is invalid for a given Pure API version.'''
    def __init__(self, *args, family_system_name, api_version, **kwargs):
        super().__init__(
            f'Invalid collection family_system_name "{family_system_name}" for api_version "{api_version}"',
            *args,
            **kwargs
        )

@frozen
class ChangeMeta:
    api_version: str = field(
        validator=[validators.instance_of(str)]
    )
    buffer_table_name: str = field(init=False)
    history_table_name: str = field(init=False)

    def __attrs_post_init__(self) -> None:
        object.__setattr__(self,'buffer_table_name', f'pure_json_change_{self.api_version}')
        object.__setattr__(self,'history_table_name', f'pure_json_change_{self.api_version}_history')

def get_change_meta(
    cursor:cx_Oracle.Cursor,
    *,
    api_version:str,
):
    '''Factory function that validates the Pure API version and returns an
    instance of ChangeCollectionMetadata. If the version is already validated,
    it is safe to instantiate the class directly, instead of calling this
    function.
    '''
    if api_version not in api_versions(cursor):
        raise(InvalidApiVersion(api_version))
    return ChangeMeta(api_version)

@frozen(kw_only=True)
class CollectionMeta:
    api_version: str = field(
        validator=[validators.instance_of(str)]
    )
    local_name: str = field(
        validator=[validators.instance_of(str)]
    )
    api_name: str = field(
        validator=[validators.instance_of(str)]
    )
    family_system_name: str = field(
        validator=[validators.instance_of(str)]
    )
    canonical_table_name: str = field(init=False)
    staging_table_name: str = field(init=False)
    change_meta: ChangeMeta = field(init=False)

    def __attrs_post_init__(self) -> None:
        object.__setattr__(self,'canonical_table_name', f'pure_json_{self.local_name}_{self.api_version}')
        object.__setattr__(self,'staging_table_name', f'pure_json_{self.local_name}_{self.api_version}_staging')
        object.__setattr__(self,'change_meta', ChangeMeta(api_version=self.api_version))

def get_collection_meta_by_local_name(
    cursor:cx_Oracle.Cursor,
    *,
    api_version:str,
    local_name:str,
):
    if api_version not in api_versions(cursor):
        raise(InvalidApiVersion(api_version))

    try:
        meta = select_unique_essential_dict(
            cursor,
            'SELECT * FROM pure_json_collection_meta WHERE local_name = :local_name AND api_version = :api_version',
            {'local_name': local_name, 'api_version': api_version}
        )
    except (NonexistentUniqueEssentialResult, MultipleUniqueEssentialResults) as e:
        raise InvalidCollectionLocalName(
            local_name=local_name,
            api_version=api_version
        )
    except Exception as e:
        raise e

    meta_lc = {k.lower(): v for k, v in meta.items()}
    return CollectionMeta(**meta_lc)

def get_collection_meta_by_api_name(
    cursor:cx_Oracle.Cursor,
    *,
    api_version:str,
    api_name:str,
):
    if api_version not in api_versions(cursor):
        raise(InvalidApiVersion(api_version))

    try:
        meta = select_unique_essential_dict(
            cursor,
            'SELECT * FROM pure_json_collection_meta WHERE api_name = :api_name AND api_version = :api_version',
            {'api_name': api_name, 'api_version': api_version}
        )
    except (NonexistentUniqueEssentialResult, MultipleUniqueEssentialResults) as e:
        raise InvalidCollectionApiName(
            api_name=api_name,
            api_version=api_version
        )
    except Exception as e:
        raise e

    meta_lc = {k.lower(): v for k, v in meta.items()}
    return CollectionMeta(**meta_lc)

def get_collection_meta_by_family_system_name(
    cursor:cx_Oracle.Cursor,
    *,
    api_version:str,
    family_system_name:str,
):
    if api_version not in api_versions(cursor):
        raise(InvalidApiVersion(api_version))

    try:
        meta = select_unique_essential_dict(
            cursor,
            'SELECT * FROM pure_json_collection_meta WHERE family_system_name = :family_system_name AND api_version = :api_version',
            {'family_system_name': family_system_name, 'api_version': api_version}
        )
    except (NonexistentUniqueEssentialResult, MultipleUniqueEssentialResults) as e:
        raise InvalidCollectionFamilySystemName(
            family_system_name=family_system_name,
            api_version=api_version
        )
    except Exception as e:
        raise e
    
    meta_lc = {k.lower(): v for k, v in meta.items()}
    return CollectionMeta(**meta_lc)

def collection_api_names_for_api_version(cursor:cx_Oracle.Cursor, *, api_version:str):
    cursor.execute(
        'SELECT DISTINCT(api_name) FROM pure_json_collection_meta where api_version = :api_version',
        {'api_version': api_version}
    )
    return [row[0] for row in cursor.fetchall()]

def collection_family_system_names_for_api_version(cursor:cx_Oracle.Cursor, *, api_version:str):
    cursor.execute(
        'SELECT DISTINCT(family_system_name) FROM pure_json_collection_meta where api_version = :api_version',
        {'api_version': api_version}
    )
    return [row[0] for row in cursor.fetchall()]
