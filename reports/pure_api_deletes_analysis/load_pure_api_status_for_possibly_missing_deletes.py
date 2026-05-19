import dotenv_switch.auto

from datetime import datetime
from itertools import batched
import re
import sys

from dateutil.parser import isoparse

from experts_dw import db
from experts_dw.cx_oracle_helpers import \
    select_list_of_scalars
from experts_dw.pure_json_collection_meta import \
    get_collection_meta_by_api_name

from pureapi import client

collection_api_name = sys.argv[1]

with db.cx_oracle_connection() as session:

    select_cursor = session.cursor()
    meta = get_collection_meta_by_api_name(
        cursor=select_cursor,
        api_version='524',
        api_name=collection_api_name,
    )
    table_name = meta.local_name + 's_possibly_missing_deletes'

    select_sql = f'select uuid from { table_name }'
    uuids = select_list_of_scalars(select_cursor, select_sql)

    update_404_sql = f'''
        UPDATE { table_name }
        SET
          pure_api_status = :pure_api_status
        WHERE uuid = :uuid
    '''

    update_200_sql = f'''
        UPDATE { table_name }
        SET
          pure_api_status = :pure_api_status,
          pure_api_created = :pure_api_created,
          pure_api_modified = :pure_api_modified,
          pure_api_returned_uuid = :pure_api_returned_uuid
        WHERE uuid = :uuid
    '''

    update_cursor = session.cursor()
    for uuid in uuids:
        try:
            r = client.get(meta.api_name + '/' + uuid, {'size':1, 'offset':0})
        except Exception as e:
            if re.search('returned HTTP status 404$', str(e)):
                update_cursor.execute(
                    update_404_sql,
                    {
                        'uuid': uuid,
                        'pure_api_status': 404,
                    }
                )
            else:
                print(f'Request for {uuid=} returned {type(e)=}: {e}')
            continue

        item = r.json()
        update_cursor.execute(
            update_200_sql,
            {
                'uuid': uuid,
                'pure_api_status': r.status_code,
                'pure_api_created': isoparse(item['info']['createdDate']),
                'pure_api_modified': isoparse(item['info']['modifiedDate']),
                'pure_api_returned_uuid': item['uuid'],
            }
        )

    session.commit()
