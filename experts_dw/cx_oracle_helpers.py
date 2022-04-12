def select_scalar(cursor, sql, params=None):
    if params is None:
        params = {}
    cursor.execute(sql, params)
    cursor.rowfactory = lambda *_tuple: _tuple[0]
    # The rowfactory will be executed only if the query returns results.
    # Otherwise, the following will return None.
    return cursor.fetchone()

def select_list_of_dicts(cursor, sql, params=None):
    if params is None:
        params = {}
    cursor.execute(sql, params)
    cursor.rowfactory = lambda *_tuple: dict(
        zip([column[0] for column in cursor.description], _tuple)
    )
    # The rowfactory will be executed only if the query returns results.
    # Otherwise, the following will return an empty list.
    return cursor.fetchall()

def select_list_of_scalars(cursor, sql, params=None):
    if params is None:
        params = {}
    cursor.execute(sql, params)
    cursor.rowfactory = lambda *_tuple: _tuple[0]
    # The rowfactory will be executed only if the query returns results.
    # Otherwise, the following will return an empty list.
    return cursor.fetchall()
