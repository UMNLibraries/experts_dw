from experts_dw.exceptions import ExpertsDwException

class InvalidKeyColumn(ValueError, ExpertsDwException):
    '''Raised when a query result that must include a key column for aggregation is missing that column.'''
    def __init__(self, *args, sql, key_column_name, params, **kwargs):
        message = f'Query result that must include key column {key_column_name} is missing that column. sql: {sql}'
        if params:
            message += f', params: {params}'
        super().__init__(
            message,
            *args,
            **kwargs
        )

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

def select_keyed_lists_of_dicts(cursor, sql, key_column_name, params=None):
    if params is None:
        params = {}

    list_of_dicts = select_list_of_dicts(cursor, sql, params=params)

    # We check only the first dict for the key column, since it should be in
    # all of them if it's in the first one:
    if len(list_of_dicts) > 0 and key_column_name not in list_of_dicts[0]:
        raise InvalidKeyColumn(
            sql=sql,
            key_column_name=key_column_name,
            params=params,
        )

    keyed_lists = {}
    for _dict in list_of_dicts:
        key = _dict[key_column_name]
        if key not in keyed_lists:
            keyed_lists[key] = []
        keyed_lists[key].append(_dict)
    return keyed_lists

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
