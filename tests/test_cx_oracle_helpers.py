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
        "SELECT last_name FROM person WHERE pure_uuid=:pure_uuid",
        {'pure_uuid': '01edf3d8-7e44-4dfa-bec4-8e3472965e1f'}
    )
    assert isinstance(last_name, str)
    assert last_name == 'Fransen'

    title = select_scalar(cursor, "SELECT title FROM pub WHERE uuid=:uuid", {'uuid': 'bogus'})
    assert title is None

    count = select_scalar(cursor, "SELECT count(*) FROM pub WHERE 1=2")
    assert count == 0

def test_select_list_of_dicts(cursor):
    rows = select_list_of_dicts(
        cursor,
        "SELECT DISTINCT p.um_acad_plan_prima, p.acad_plan_sdesc, \
        p.acad_plan_ldesc, p.deptid, u.pure_org_uuid \
        FROM ps_dwsa_stix_1223_pr@dweprd.oit p \
            JOIN umn_dept_pure_org u \
            ON p.deptid = u.deptid \
        WHERE level2 = 'GRAD' OR level2 = 'PRFL'"
    )
    assert isinstance(rows, list)

    row = rows[0]
    assert isinstance(row, dict)

    plan = row.get('ACAD_PLAN_SDESC', None)
    assert isinstance(plan, str)

    rows = select_list_of_dicts(cursor, "SELECT DISTINCT um_acad_plan_prima FROM ps_dwsa_stix_1223_pr@dweprd.oit WHERE level2='BOGUS'")
    # Test for empty list
    assert rows is None

def test_select_list_of_scalars(cursor):
    rows = select_list_of_scalars(
    cursor,
    "SELECT DISTINCT(api_version) FROM pure_json_collection_meta"
    )
    assert isinstance(rows, list)

    row = rows[0]
    assert isinstance(row, tuple)

    api_version = select_list_of_scalars(cursor, "SELECT DISTINCT(api_version) FROM pure_json_collection_meta WHERE 1=2")
    assert api_version is None


   # row = rows[0]
    #assert isinstance(row, dict)

  #  plan = row.get('ACAD_PLAN_SDESC', None)
   # assert isinstance(plan, str)


#with db.cx_oracle_connection() as connection:
#    cur = connection.cursor()
#
#    cur.execute("SELECT * FROM pub WHERE 1=2")
#    cur.rowfactory = lambda *args: dict(
#        zip([col[0] for col in cur.description], args)
#    )
#    rows = cur.fetchall()
#    print('    ',rows) # []
#
#    cur.execute("SELECT last_name FROM person WHERE pure_uuid='01edf3d8-7e44-4dfa-bec4-8e3472965e1f'")
#    result = cur.fetchone()
#    print('    ',result) #
#
#    cur.execute("SELECT title FROM pub WHERE uuid='bogus'")
#    result = cur.fetchone()
#    print('    ',result) #
#    title = cur.fetchone()[0]
#    print('    ',title) # NoneType is not subscriptable
#
#    cur.execute("SELECT count(*) FROM pub WHERE 1=2")
#    count = cur.fetchone()[0]
#    print('    ',count) # 0
#
#    cur.execute("SELECT * FROM bogus WHERE 1=2") # "table or view does not exist" exception
#    cur.rowfactory = lambda *args: dict(
#        zip([col[0] for col in cur.description], args)
#    )
#    rows = cur.fetchall()
#    print('    ',rows)
#
