import dotenv_switch.auto

from datetime import datetime
from itertools import batched
import sys

from dateutil.parser import isoparse

from experts_dw import db
from experts_dw.pure_json_collection_meta import \
    get_collection_meta_by_api_name

from pureapi import client

start_date_str = sys.argv[1]
end_date_str = sys.argv[2]
collection_api_name = sys.argv[3]

created_after_before_payload = {
  'offset': 0,
  'createdAfter':  f'{start_date_str}T00:00:00.525Z',
  'createdBefore': f'{end_date_str}T00:00:00.525Z',
}

rows_per_insert = 1000

with db.cx_oracle_connection() as session:

    meta = get_collection_meta_by_api_name(
        cursor=session.cursor(),
        api_version='524',
        api_name=collection_api_name,
    )

    insert_sql = f'''
        INSERT INTO pure_api_{ meta.local_name }_created_between_2025_2026_02_03
        (
          uuid,
          inserted,
          updated,
          pure_created,
          pure_modified
        ) VALUES (
          :uuid,
          :inserted,
          :updated,
          :pure_created,
          :pure_modified
        )
    '''

    cur = session.cursor()
    for batch in list(batched(
        [
            {
                'uuid': item.uuid,
                'pure_created': isoparse(item.info.createdDate),
                'pure_modified': isoparse(item.info.modifiedDate),
                'inserted': datetime.now(),
                'updated': datetime.now(),


            }
            for item in client.filter_all_transformed(
                meta.api_name,
                payload=created_after_before_payload,
                config=client.Config()
            )
        ],
        rows_per_insert
    )):
        cur.executemany(insert_sql, list(batch))
        session.commit()
