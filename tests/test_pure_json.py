import dotenv_switch.auto

import pytest

from experts_dw import db
from experts_dw.pure_json import \
    get_change_table_name, \
    get_collection_table_name \

@pytest.fixture
def connection():
    with db.cx_oracle_connection() as connection:
        yield connection

@pytest.fixture
def cursor(connection):
    return connection.cursor()

def test_get_change_table_name():
    assert get_change_table_name(
        api_version='524'
    ) == 'pure_json_change_524'
    assert get_change_table_name(
        api_version='524',
        history=True
    ) == 'pure_json_change_524_history'

def test_get_collection_table_name():
    assert get_collection_table_name(
        api_version='524',
        collection_local_name='person'
    ) == 'pure_json_person_524'
    assert get_collection_table_name(
        api_version='524',
        collection_local_name='person',
        staging=True
    ) == 'pure_json_person_524_staging'
