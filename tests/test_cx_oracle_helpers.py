import dotenv_switch.auto

import pytest

from experts_dw import db
from experts_dw.cx_oracle_helpers import select_scalar, select_list_of_dicts, select_list_of_scalars

@pytest.fixture
def connection():
    with db.cx_oracle_connection() as connection:
        yield connection

@pytest.fixture
def cursor(connection):
    return connection.cursor()

def test_select_scalar(cursor):
    last_name = select_scalar(
        cursor,
        'SELECT last_name FROM person WHERE pure_uuid=:pure_uuid',
        {'pure_uuid': '01edf3d8-7e44-4dfa-bec4-8e3472965e1f'}
    )
    assert isinstance(last_name, str)
    assert last_name == 'Fransen'

    title = select_scalar(
        cursor,
        'SELECT title FROM pub WHERE uuid=:uuid',
        {'uuid': 'bogus'}
    )
    assert title is None

    count = select_scalar(cursor, 'SELECT count(*) FROM pub WHERE 1=2')
    assert count == 0

def test_select_list_of_dicts(cursor):
    metadata = select_list_of_dicts(
        cursor,
        'SELECT * FROM pure_json_collection_meta'
    )
    assert isinstance(metadata, list)
    for collection in metadata:
        assert isinstance(collection, dict)
        assert set(collection.keys()) == {'API_NAME','API_VERSION','FAMILY_SYSTEM_NAME','LOCAL_NAME'}
        assert all(isinstance(value, str) for value in collection.values())

    empty_metadata = select_list_of_dicts(
        cursor,
        'SELECT * FROM pure_json_collection_meta WHERE api_name=:api_name',
        {'api_name': 'bogus'}
    )
    assert isinstance(empty_metadata, list)
    assert len(empty_metadata) == 0

def test_select_list_of_scalars(cursor):
    versions = select_list_of_scalars(
        cursor,
        'SELECT DISTINCT(api_version) FROM pure_json_collection_meta'
    )
    print(versions)
    assert isinstance(versions, list)
    assert all(isinstance(version, str) for version in versions)

    person_versions = select_list_of_scalars(
        cursor,
        'SELECT DISTINCT(api_version) FROM pure_json_collection_meta where local_name=:local_name',
        {'local_name': 'person'}
    )
    assert isinstance(person_versions, list)
    assert all(isinstance(person_version, str) for person_version in person_versions)

    no_versions = select_list_of_scalars(
        cursor,
        'SELECT DISTINCT(api_version) FROM pure_json_collection_meta WHERE api_name=:api_name',
        {'api_name': 'bogus'}
    )
    assert isinstance(no_versions, list)
    assert len(no_versions) == 0
