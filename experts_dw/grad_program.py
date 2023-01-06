import datetime
from datetime import date
import functools
import re
from typing import Any, Callable, MutableMapping, Tuple, TypeVar, cast

from experts_dw.cx_oracle_helpers import select_list_of_scalars

term_table_prefix = 'PS_DWSA_STIX_1'
term_table_suffixes = ['9_PR','5','5_INT','3_PR']

F = TypeVar('F', bound=Callable[..., Any])

def valid_year(year: str) -> bool:
    return \
        re.match(r'^\d\d$', year) and \
        int(year) >= 0 and \
        int(year) <= int(current_year())

def current_year() -> str:
    # The strftime call returns a two-digit year.
    return date.today().strftime('%y') 

def previous_year() -> str:
    # The [-2:] selects the last two elements of the array of characters,
    # giving us a two-digit year.
    return str((date.today().year - 1))[-2:]

def validate_year(func: F) -> F:
    '''A decorator wrapper that validates the year component of a STIX table suffix.

    Args:
        func: The function to be wrapped.

    Return:
        The wrapped function.

    Raises:
        PureAPIMissingVersionError: If the ``version`` kwarg is missing or
            the value is None.
        PureAPIInvalidVersionError: If the ``version`` is unrecognized.
    '''
    @functools.wraps(func)
    def wrapper_validate_year(*args, **kwargs):
        if 'year' in kwargs and kwargs['year'] is not None:
            if not valid_year(kwargs['year']):
                #raise PureAPIInvalidVersionError(kwargs['year'])
                raise Exception
        else:
            kwargs['year'] = current_year()
        return func(*args, **kwargs)
    return cast(F, wrapper_validate_year)

@validate_year
def term_table_names(*, year : str = None) -> Tuple[str]:
    return [f'{term_table_prefix}{year}{suffix}' for suffix in term_table_suffixes]

def latest_term_table_name(cursor) -> str:
    existing_db_table_names = select_list_of_scalars(
       cursor,
       f"SELECT table_name FROM all_tables@dweprd.oit WHERE table_name LIKE '{term_table_prefix}%'",
    )
    return next(
        (table_name
            for table_name
            in term_table_names(year=current_year()) + term_table_names(year=previous_year())
            if table_name in existing_db_table_names
        ), None
    )
