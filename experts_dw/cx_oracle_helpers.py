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
    result = cursor.fetchall()
    return result
