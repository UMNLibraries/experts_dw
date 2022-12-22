from datetime import date
import functools
import re
from typing import Any, Callable, MutableMapping, Tuple, TypeVar, cast

F = TypeVar('F', bound=Callable[..., Any])

def valid_year(year: str) -> bool:
    return \
        re.match(r'^\d\d$', year) and \
        int(year) >= 0 and \
        int(year) <= int(current_year())

def current_year() -> str:
    return date.today().strftime('%y') # two-digit year

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
def term_table_suffixes(*, year : str = None) -> Tuple[str]:
    return [f'1{year}{suffix}' for suffix in ['3_PR','5_INT','5','9_PR']]
