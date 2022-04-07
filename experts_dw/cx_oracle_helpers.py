def select_scalar(cursor, sql, params=None):
    if params is None:
        params = {}
    cursor.execute(sql, params)
    result = cursor.fetchone()
    if result is None:
        return result
    else:
        return result[0] # Result will be a tuple

def select_list_of_dicts(cursor, sql, params=None):
    if params is None:
        params = {}
    cursor.execute(sql, params)
    cursor.rowfactory = lambda *args: dict(
        zip([col[0] for col in cursor.description], args)
    )
    result = cursor.fetchall() # Result will be a list of dicts
    if bool(result) is False: # Empty list is False
        return None
    else:
        return result

def select_list_of_scalars(cursor, sql, params=None):
    if params is None:
        params = {}
    cursor.execute(sql, params)
    result = cursor.fetchall()
    if bool(result) is False:
        return None
    else:
        return result
