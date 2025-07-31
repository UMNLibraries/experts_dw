from experts_dw.exceptions import ExpertsDwException

class NonexistentUniqueEssentialResult(ValueError, ExpertsDwException):
    '''Raised when a query that must return a single row returns zero rows.'''
    def __init__(self, *args, sql, params, **kwargs):
        message = f'Query that must return a single row returned zero rows. sql: {sql}'
        if params:
            message += f', params: {params}'
        super().__init__(
            message,
            *args,
            **kwargs
        )

class MultipleUniqueEssentialResults(ValueError, ExpertsDwException):
    '''Raised when a query that must return a single row returns multiple rows.'''
    def __init__(self, *args, sql, params, **kwargs):
        message = f'Query that must return a single row returned multiple rows. sql: {sql}'
        if params:
            message += f', params: {params}'
        super().__init__(
            message,
            *args,
            **kwargs
        )

def select_scalar(cursor, sql, params=None):
    if params is None:
        params = {}
    cursor.execute(sql, params)
    cursor.rowfactory = lambda *_tuple: _tuple[0]
    # The rowfactory will be executed only if the query returns results.
    # Otherwise, the following will return None.
    return cursor.fetchone()

def select_list_of_scalars(cursor, sql, params=None):
    if params is None:
        params = {}
    cursor.execute(sql, params)
    cursor.rowfactory = lambda *_tuple: _tuple[0]
    # The rowfactory will be executed only if the query returns results.
    # Otherwise, the following will return an empty list.
    return cursor.fetchall()

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

def select_unique_essential_dict(cursor, sql, params=None):
    dicts = select_list_of_dicts(cursor, sql, params)
    dicts_count = sum(1 for _dict in dicts if isinstance(_dict, dict))
    if dicts_count == 0:
        raise NonexistentUniqueEssentialResult(
            sql=sql,
            params=params,
        )
    elif dicts_count > 1:
        raise MultipleUniqueEssentialResults(
            sql=sql,
            params=params,
        )
    return dicts[0]
