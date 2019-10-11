# coding=utf-8

__author__ = 'sinlov'

import inspect
import warnings
from functools import wraps

string_types = (type(b''), type(u''))


def deprecated(reason):
    """
    use as
    @deprecated('method reason')


    warning support python 2.6.+
    :param reason: reason of deprecate
    """
    if isinstance(reason, string_types):

        def decorator(func1):

            if inspect.isclass(func1):
                fmt1 = "Call to deprecated class {name} ({reason})."
            else:
                fmt1 = "Call to deprecated function {name} ({reason})."

            @wraps(func1)
            def new_func1(*args, **kwargs):
                warnings.simplefilter('always', DeprecationWarning)
                warnings.warn(
                    fmt1.format(name=func1.__name__, reason=reason),
                    category=DeprecationWarning,
                    stacklevel=2
                )
                warnings.simplefilter('default', DeprecationWarning)
                return func1(*args, **kwargs)

            # Enhance docstring with a deprecation note
            deprecation_note = "\n\n.. note::\n    Deprecated: " + reason
            if new_func1.__doc__:
                new_func1.__doc__ += deprecation_note
            else:
                new_func1.__doc__ = deprecation_note
            return new_func1

        return decorator

    elif inspect.isclass(reason) or inspect.isfunction(reason):
        raise TypeError("Reason for deprecation must be supplied")

    else:
        raise TypeError(repr(type(reason)))
