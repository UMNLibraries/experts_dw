import dotenv_switch.auto

from experts_dw import db, pure_json

sql_hint_select_where = f'''
INSERT /*+ ignore_row_on_dupkey_index(pure_json_person_524_staging(uuid, pure_modified)) */ 
INTO pure_json_person_524_staging
(
  uuid,
  pure_created,
  pure_modified,
  inserted,
  updated,
  json_document
) SELECT
  :uuid,
  :pure_created,
  :pure_modified,
  :inserted,
  :updated,
  :json_document
FROM pure_json_person_524_staging 
WHERE NOT EXISTS (
  SELECT 1 FROM pure_json_person_524_staging
  WHERE uuid = :uuid AND pure_modified = :pure_modified
)
'''

sql_select_where = f'''
INSERT
INTO pure_json_person_524_staging
(
  uuid,
  pure_created,
  pure_modified,
  inserted,
  updated,
  json_document
) SELECT
  :uuid,
  :pure_created,
  :pure_modified,
  :inserted,
  :updated,
  :json_document
FROM pure_json_person_524_staging 
WHERE NOT EXISTS (
  SELECT 1 FROM pure_json_person_524_staging
  WHERE uuid = :uuid AND pure_modified = :pure_modified
)
'''

sql_hint_select = f'''
INSERT /*+ ignore_row_on_dupkey_index(pure_json_person_524_staging(uuid, pure_modified)) */ 
INTO pure_json_person_524_staging
(
  uuid,
  pure_created,
  pure_modified,
  inserted,
  updated,
  json_document
) SELECT
  :uuid,
  :pure_created,
  :pure_modified,
  :inserted,
  :updated,
  :json_document
FROM pure_json_person_524_staging 
'''

sql_hint_values = f'''
INSERT /*+ ignore_row_on_dupkey_index(pure_json_person_524_staging(uuid, pure_modified)) */ 
INTO pure_json_person_524_staging
(
  uuid,
  pure_created,
  pure_modified,
  inserted,
  updated,
  json_document
) VALUES (
  :uuid,
  :pure_created,
  :pure_modified,
  :inserted,
  :updated,
  :json_document
)
'''

sql_select = f'''
INSERT
INTO pure_json_person_524_staging
(
  uuid,
  pure_created,
  pure_modified,
  inserted,
  updated,
  json_document
) SELECT
  :uuid,
  :pure_created,
  :pure_modified,
  :inserted,
  :updated,
  :json_document
FROM pure_json_person_524_staging 
'''

sql_values = f'''
INSERT
INTO pure_json_person_524_staging
(
  uuid,
  pure_created,
  pure_modified,
  inserted,
  updated,
  json_document
) VALUES (
  :uuid,
  :pure_created,
  :pure_modified,
  :inserted,
  :updated,
  :json_document
)
'''

with db.cx_oracle_connection() as session:
    cur = session.cursor()

    uuid = 'ae9a2751-d117-4eb5-9a2e-95188a0d2c96';
    cur.execute(f"SELECT * FROM pure_json_person_524 WHERE uuid = '{uuid}'")
    columns = [col[0].lower() for col in cur.description]
    cur.rowfactory = lambda *args: dict(zip(columns, args))
    record = cur.fetchone()
    #print(record)

#    sql = pure_json.insert_sql(
#        cur,
#        api_version='524',
#        collection_local_name='person',
#        staging=True
#    )
#    print(sql)
#   cur.execute(sql, record)
    cur.execute(sql_hint_select_where, record)

    cur.execute(f"SELECT * FROM pure_json_person_524_staging WHERE uuid = '{uuid}'")
    columns = [col[0].lower() for col in cur.description]
    cur.rowfactory = lambda *args: dict(zip(columns, args))
    record = cur.fetchone()
    #print(record)

    # Try inserting again, using multiple insert variations:
    try:
        cur.execute(sql_hint_select_where, record)
    except Exception as e:
        error_obj, = e.args
        print('An attempt to re-insert the same record, using a hint and a select where, generated this error: ', error_obj.message)
    else:
        print('An attempt to re-insert the same record, using a hint and a select where, was ignored without errors')

    try:
        cur.execute(sql_select_where, record)
    except Exception as e:
        error_obj, = e.args
        print('An attempt to re-insert the same record, using a select where, generated this error: ', error_obj.message)
    else:
        print('An attempt to re-insert the same record, using a select where, was ignored without errors')

    try:
        cur.execute(sql_hint_select, record)
    except Exception as e:
        error_obj, = e.args
        print('An attempt to re-insert the same record, using a hint and a select, generated this error: ', error_obj.message)
    else:
        print('An attempt to re-insert the same record, using a hint and a select where, was ignored without errors')

    try:
        cur.execute(sql_hint_values, record)
    except Exception as e:
        error_obj, = e.args
        print('An attempt to re-insert the same record, using a hint and values, generated this error: ', error_obj.message)
    else:
        print('An attempt to re-insert the same record, using a hint and values, was ignored without errors')

    try:
        cur.execute(sql_select, record)
    except Exception as e:
        error_obj, = e.args
        print('An attempt to re-insert the same record, using a select, generated this error: ', error_obj.message)
    else:
        print('An attempt to re-insert the same record, using a select where, was ignored without errors')

    try:
        cur.execute(sql_values, record)
    except Exception as e:
        error_obj, = e.args
        print('An attempt to re-insert the same record, using values, generated this error: ', error_obj.message)
    else:
        print('An attempt to re-insert the same record, using values, was ignored without errors')

    # If we don't commit, the update won't be saved.
    #session.commit()
