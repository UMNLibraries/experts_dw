from attrs import field, frozen, validators

import cx_Oracle

from experts_dw import db
from experts_dw.cx_oracle_helpers import \
    select_unique_essential_dict, \
    NonexistentUniqueEssentialResult, \
    MultipleUniqueEssentialResults
from experts_dw.exceptions import ExpertsDwException

class InvalidCollectionLocalName(ValueError, ExpertsDwException):
    '''Raised when a local collection name is invalid.'''
    def __init__(self, *args, local_name, **kwargs):
        super().__init__(
            f'Invalid local_name "{local_name}"',
            *args,
            **kwargs
        )

class InvalidCollectionApiName(ValueError, ExpertsDwException):
    '''Raised when a Scopus API collection name is invalid.'''
    def __init__(self, *args, api_name, **kwargs):
        super().__init__(
            f'Invalid api_name "{api_name}"',
            *args,
            **kwargs
        )

class InvalidCollectionSchemaRecordName(ValueError, ExpertsDwException):
    '''Raised when a Scopus API schema record name is invalid.'''
    def __init__(self, *args, schema_record_name, **kwargs):
        super().__init__(
            f'Invalid schema_record_name "{schema_record_name}"',
            *args,
            **kwargs
        )

@frozen(kw_only=True)
class CollectionMeta:
    local_name: str = field(
        validator=[validators.instance_of(str)]
    )
    api_name: str = field(
        validator=[validators.instance_of(str)]
    )
    schema_record_name: str = field(
        validator=[validators.instance_of(str)]
    )
    canonical_table_name: str = field(init=False)
    staging_table_name: str = field(init=False)

    def __attrs_post_init__(self) -> None:
        object.__setattr__(self,'canonical_table_name', f'scopus_json_{self.local_name}')
        object.__setattr__(self,'staging_table_name', f'scopus_json_{self.local_name}_staging')

def get_collection_meta_by_local_name(
    cursor:cx_Oracle.Cursor,
    *,
    local_name:str,
):
    try:
        meta = select_unique_essential_dict(
            cursor,
            'SELECT * FROM scopus_json_collection_meta WHERE local_name = :local_name',
            {'local_name': local_name}
        )
    except (NonexistentUniqueEssentialResult, MultipleUniqueEssentialResults) as e:
        raise InvalidCollectionLocalName(
            local_name=local_name,
        )
    except Exception as e:
        raise e

    meta_lc = {k.lower(): v for k, v in meta.items()}
    return CollectionMeta(**meta_lc)

def get_collection_meta_by_api_name(
    cursor:cx_Oracle.Cursor,
    *,
    api_name:str,
):
    try:
        meta = select_unique_essential_dict(
            cursor,
            'SELECT * FROM scopus_json_collection_meta WHERE api_name = :api_name',
            {'api_name': api_name}
        )
    except (NonexistentUniqueEssentialResult, MultipleUniqueEssentialResults) as e:
        raise InvalidCollectionApiName(
            api_name=api_name,
        )
    except Exception as e:
        raise e

    meta_lc = {k.lower(): v for k, v in meta.items()}
    return CollectionMeta(**meta_lc)

def get_collection_meta_by_schema_record_name(
    cursor:cx_Oracle.Cursor,
    *,
    schema_record_name:str,
):
    try:
        meta = select_unique_essential_dict(
            cursor,
            'SELECT * FROM scopus_json_collection_meta WHERE schema_record_name = :schema_record_name',
            {'schema_record_name': schema_record_name}
        )
    except (NonexistentUniqueEssentialResult, MultipleUniqueEssentialResults) as e:
        raise InvalidCollectionSchemaRecordName(
            schema_record_name=schema_record_name,
        )
    except Exception as e:
        raise e
    
    meta_lc = {k.lower(): v for k, v in meta.items()}
    return CollectionMeta(**meta_lc)
