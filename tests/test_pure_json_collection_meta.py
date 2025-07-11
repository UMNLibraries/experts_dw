import dotenv_switch.auto

from attrs import asdict
import pytest

from experts_dw import db
from experts_dw.pure_json_collection_meta import \
    ChangeMeta, \
    CollectionMeta, \
    InvalidApiVersion, \
    InvalidCollectionLocalName, \
    InvalidCollectionApiName, \
    InvalidCollectionFamilySystemName, \
    get_change_meta, \
    get_collection_meta_by_local_name, \
    get_collection_meta_by_api_name, \
    get_collection_meta_by_family_system_name \

change_meta_524 = ChangeMeta(api_version='524')

@pytest.fixture
def connection():
    with db.cx_oracle_connection() as connection:
        yield connection

@pytest.fixture
def cursor(connection):
    return connection.cursor()

def test_get_change_meta(cursor):
    meta = get_change_meta(
        cursor=cursor,
        api_version='524',
    )
    assert isinstance(meta, ChangeMeta)
    assert asdict(meta) == {
        'api_version': '524',
        'buffer_table_name': 'pure_json_change_524',
        'history_table_name': 'pure_json_change_524_history',
    } 
    assert asdict(meta) == asdict(change_meta_524) # Sanity check of the latter, since we will use it in later tests.
    with pytest.raises(InvalidApiVersion):
        meta = get_change_meta(
            cursor=cursor,
            api_version='bogus',
        )

def test_get_collection_meta_by_local_name(cursor):
    meta = get_collection_meta_by_local_name(
        cursor=cursor,
        api_version='524',
        local_name='person',
    )
    assert isinstance(meta, CollectionMeta)
    assert isinstance(meta.change_meta, ChangeMeta)
    meta_asdict = asdict(meta)
    meta_asdict['change_meta'] = asdict(meta.change_meta)
    assert meta_asdict == {
        'api_version': '524',
        'local_name': 'person',
        'api_name': 'persons',
        'family_system_name': 'Person',
        'canonical_table_name': 'pure_json_person_524',
        'staging_table_name': 'pure_json_person_524_staging',
        'change_meta': asdict(change_meta_524),
    } 
    with pytest.raises(InvalidApiVersion):
        meta = get_collection_meta_by_local_name(
            cursor=cursor,
            api_version='bogus',
            local_name='person',
        )
    with pytest.raises(InvalidCollectionLocalName):
        meta = get_collection_meta_by_local_name(
            cursor=cursor,
            api_version='524',
            local_name='bogus',
        )

def test_get_collection_meta_by_api_name(cursor):
    meta = get_collection_meta_by_api_name(
        cursor=cursor,
        api_version='524',
        api_name='organisational-units',
    )
    assert isinstance(meta, CollectionMeta)
    assert isinstance(meta.change_meta, ChangeMeta)
    meta_asdict = asdict(meta)
    meta_asdict['change_meta'] = asdict(meta.change_meta)
    assert meta_asdict == {
        'api_version': '524',
        'local_name': 'organisation',
        'api_name': 'organisational-units',
        'family_system_name': 'Organisation',
        'canonical_table_name': 'pure_json_organisation_524',
        'staging_table_name': 'pure_json_organisation_524_staging',
        'change_meta': asdict(change_meta_524),
    }
    with pytest.raises(InvalidCollectionApiName):
        meta = get_collection_meta_by_api_name(
            cursor=cursor,
            api_version='524',
            api_name='bogus',
        )

def test_get_collection_meta_by_family_system_name(cursor):
    meta = get_collection_meta_by_family_system_name(
        cursor=cursor,
        api_version='524',
        family_system_name='ResearchOutput',
    )
    assert isinstance(meta, CollectionMeta)
    assert isinstance(meta.change_meta, ChangeMeta)
    meta_asdict = asdict(meta)
    meta_asdict['change_meta'] = asdict(meta.change_meta)
    assert meta_asdict == {
        'api_version': '524',
        'local_name': 'research_output',
        'api_name': 'research-outputs',
        'family_system_name': 'ResearchOutput',
        'canonical_table_name': 'pure_json_research_output_524',
        'staging_table_name': 'pure_json_research_output_524_staging',
        'change_meta': asdict(change_meta_524),
    }
    with pytest.raises(InvalidCollectionFamilySystemName):
        meta = get_collection_meta_by_family_system_name(
            cursor=cursor,
            api_version='524',
            family_system_name='Bogus',
        )
