import dotenv_switch.auto

from attrs import asdict
import pytest

from experts_dw import db
from experts_dw.pure_json_collection_metadata import \
    ChangeCollectionMetadata, \
    SingleCollectionMetadata, \
    InvalidApiVersion, \
    InvalidCollectionLocalName, \
    InvalidCollectionApiName, \
    InvalidCollectionFamilySystemName, \
    get_change_collection_metadata, \
    get_single_collection_metadata_by_local_name, \
    get_single_collection_metadata_by_api_name, \
    get_single_collection_metadata_by_family_system_name \

@pytest.fixture
def connection():
    with db.cx_oracle_connection() as connection:
        yield connection

@pytest.fixture
def cursor(connection):
    return connection.cursor()

def test_get_change_collection_metadata(cursor):
    meta = get_change_collection_metadata(
        cursor=cursor,
        api_version='524',
    )
    assert isinstance(meta, ChangeCollectionMetadata)
    assert asdict(meta) == {
        'api_version': '524',
        'buffer_table_name': 'pure_json_change_524',
        'history_table_name': 'pure_json_change_524_history',
    } 
    with pytest.raises(InvalidApiVersion):
        meta = get_change_collection_metadata(
            cursor=cursor,
            api_version='bogus',
        )

def test_get_single_collection_metadata_by_local_name(cursor):
    meta = get_single_collection_metadata_by_local_name(
        cursor=cursor,
        api_version='524',
        local_name='person',
    )
    assert isinstance(meta, SingleCollectionMetadata)
    assert asdict(meta) == {
        'api_version': '524',
        'local_name': 'person',
        'api_name': 'persons',
        'family_system_name': 'Person',
        'canonical_table_name': 'pure_json_person_524',
        'staging_table_name': 'pure_json_person_524_staging',
    } 
    with pytest.raises(InvalidApiVersion):
        meta = get_single_collection_metadata_by_local_name(
            cursor=cursor,
            api_version='bogus',
            local_name='person',
        )
    with pytest.raises(InvalidCollectionLocalName):
        meta = get_single_collection_metadata_by_local_name(
            cursor=cursor,
            api_version='524',
            local_name='bogus',
        )

def test_get_single_collection_metadata_by_api_name(cursor):
    meta = get_single_collection_metadata_by_api_name(
        cursor=cursor,
        api_version='524',
        api_name='organisational-units',
    )
    assert isinstance(meta, SingleCollectionMetadata)
    assert asdict(meta) == {
        'api_version': '524',
        'local_name': 'organisation',
        'api_name': 'organisational-units',
        'family_system_name': 'Organisation',
        'canonical_table_name': 'pure_json_organisation_524',
        'staging_table_name': 'pure_json_organisation_524_staging',
    }
    with pytest.raises(InvalidCollectionApiName):
        meta = get_single_collection_metadata_by_api_name(
            cursor=cursor,
            api_version='524',
            api_name='bogus',
        )

def test_get_single_collection_metadata_by_family_system_name(cursor):
    meta = get_single_collection_metadata_by_family_system_name(
        cursor=cursor,
        api_version='524',
        family_system_name='ResearchOutput',
    )
    assert isinstance(meta, SingleCollectionMetadata)
    assert asdict(meta) == {
        'api_version': '524',
        'local_name': 'research_output',
        'api_name': 'research-outputs',
        'family_system_name': 'ResearchOutput',
        'canonical_table_name': 'pure_json_research_output_524',
        'staging_table_name': 'pure_json_research_output_524_staging',
    }
    with pytest.raises(InvalidCollectionFamilySystemName):
        meta = get_single_collection_metadata_by_family_system_name(
            cursor=cursor,
            api_version='524',
            family_system_name='Bogus',
        )
