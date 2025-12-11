import dotenv_switch.auto

from attrs import asdict
import pytest

from experts_dw import db
from experts_dw.scopus_json_collection_meta import \
    CollectionMeta, \
    InvalidCollectionLocalName, \
    InvalidCollectionApiName, \
    InvalidCollectionSchemaRecordName, \
    get_collection_meta_by_local_name, \
    get_collection_meta_by_api_name, \
    get_collection_meta_by_schema_record_name \

@pytest.fixture
def connection():
    with db.cx_oracle_connection() as connection:
        yield connection

@pytest.fixture
def cursor(connection):
    return connection.cursor()

def test_get_collection_meta_by_local_name(cursor):
    meta = get_collection_meta_by_local_name(
        cursor=cursor,
        local_name='abstract',
    )
    assert isinstance(meta, CollectionMeta)
    assert asdict(meta) == {
        'local_name': 'abstract',
        'api_name': 'abstract',
        'schema_record_name': 'abstracts-retrieval-response',
        'canonical_table_name': 'scopus_json_abstract',
        'staging_table_name': 'scopus_json_abstract_staging',
        'defunct_table_name': 'scopus_abstract_defunct',
        'to_download_table_name': 'scopus_abstract_to_download',
    } 
    with pytest.raises(InvalidCollectionLocalName):
        meta = get_collection_meta_by_local_name(
            cursor=cursor,
            local_name='bogus',
        )

def test_get_collection_meta_by_api_name(cursor):
    meta = get_collection_meta_by_api_name(
        cursor=cursor,
        api_name='abstract/citations',
    )
    assert isinstance(meta, CollectionMeta)
    assert asdict(meta) == {
        'local_name': 'citation',
        'api_name': 'abstract/citations',
        'schema_record_name': 'abstract-citations-response',
        'canonical_table_name': 'scopus_json_citation',
        'staging_table_name': 'scopus_json_citation_staging',
        'defunct_table_name': 'scopus_citation_defunct',
        'to_download_table_name': 'scopus_citation_to_download',
    }
    with pytest.raises(InvalidCollectionApiName):
        meta = get_collection_meta_by_api_name(
            cursor=cursor,
            api_name='bogus',
        )

def test_get_collection_meta_by_schema_record_name(cursor):
    meta = get_collection_meta_by_schema_record_name(
        cursor=cursor,
        schema_record_name='abstracts-retrieval-response',
    )
    assert isinstance(meta, CollectionMeta)
    assert asdict(meta) == {
        'local_name': 'abstract',
        'api_name': 'abstract',
        'schema_record_name': 'abstracts-retrieval-response',
        'canonical_table_name': 'scopus_json_abstract',
        'staging_table_name': 'scopus_json_abstract_staging',
        'defunct_table_name': 'scopus_abstract_defunct',
        'to_download_table_name': 'scopus_abstract_to_download',
    }
    with pytest.raises(InvalidCollectionSchemaRecordName):
        meta = get_collection_meta_by_schema_record_name(
            cursor=cursor,
            schema_record_name='bogus',
        )
