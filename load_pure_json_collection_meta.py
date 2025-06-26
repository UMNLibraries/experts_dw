import dotenv_switch.auto
from datetime import datetime
from jinja2 import Template
import json
import sys

from experts_dw import db
#from experts_dw import pure_json
#from experts_dw.sqlapi import sqlapi

def pure_json_insert_sql():
    return '''
        INSERT INTO pure_json_collection_meta
        (
          api_name,
          api_version,
          family_system_name,
          local_name
        ) VALUES (
          :api_name,
          :api_version,
          :family_system_name,
          :local_name
        )
    '''

#api_version = '516'
#api_version = '517'
#api_version = '518'
#api_version = '523'
api_version = '524'

with db.cx_oracle_connection() as session:
    cur = session.cursor()
    collections_to_insert = []
    insert_sql = pure_json_insert_sql()
    #print(insert_sql)
    collections_to_insert = [
        {
            'api_name': 'external-organisations',
            'api_version': api_version,
            'family_system_name': 'ExternalOrganisation',
            'local_name': 'external_organisation',
        },
        {
            'api_name': 'external-persons',
            'api_version': api_version,
            'family_system_name': 'ExternalPerson',
            'local_name': 'external_person',
        },
        {
            'api_name': 'organisational-units',
            'api_version': api_version,
            'family_system_name': 'Organisation',
            'local_name': 'organisation',
        },
        {
            'api_name': 'persons',
            'api_version': api_version,
            'family_system_name': 'Person',
            'local_name': 'person',
        },
        {
            'api_name': 'journals',
            'api_version': api_version,
            'family_system_name': 'Journal',
            'local_name': 'journal',
        },
        {
            'api_name': 'research-outputs',
            'api_version': api_version,
            'family_system_name': 'ResearchOutput',
            'local_name': 'research_output',
        },
    ]
    cur.executemany(insert_sql, collections_to_insert)
    session.commit()
