import dotenv_switch.auto

from experts_dw import db

def scopus_json_insert_sql():
    return '''
        INSERT INTO scopus_json_collection_meta
        (
          api_name,
          schema_record_name,
          local_name
        ) VALUES (
          :api_name,
          :schema_record_name,
          :local_name
        )
    '''
with db.cx_oracle_connection() as session:
    cur = session.cursor()
    collections_to_insert = []
    insert_sql = scopus_json_insert_sql()
    collections_to_insert = [
        {
            'api_name': 'abstract',
            'schema_record_name': 'abstracts-retrieval-response',
            'local_name': 'abstract',
        },
    ]
    cur.executemany(insert_sql, collections_to_insert)
    session.commit()
