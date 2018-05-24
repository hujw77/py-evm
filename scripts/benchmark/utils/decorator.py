import logging
import os
import timeit

from typing import (
    Any,
    Callable
)


def default_format(val: str) -> str:
    return val


# TODO: This is a rip off from profilehooks. Clean this up

def timecall(
        fn: Callable[..., Any]=None,
        log_level: int=logging.INFO,
        formatter: Callable[[str], str]=default_format) -> Callable[..., Any]:

    if fn is None:  # @timecall() syntax -- we are a decorator maker
        def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            return timecall(fn, log_level=log_level, formatter=formatter)
        return decorator

    # @timecall syntax -- we are a decorator.
    fp = FuncTimer(fn, log_level=log_level, formatter=formatter)

    # We cannot return fp or fp.__call__ directly as that would break method
    # definitions, instead we need to return a plain function.
    def new_fn(*args: Any, **kw: Any) -> Any:
        return fp(*args, **kw)
    new_fn.__doc__ = fn.__doc__
    new_fn.__name__ = fn.__name__
    new_fn.__dict__ = fn.__dict__
    new_fn.__module__ = fn.__module__
    return new_fn


class FuncTimer(object):

    def __init__(
            self,
            fn: Callable[..., Any],
            log_level: int, formatter: Callable[[str], str]) -> None:

        self.fn = fn
        self.ncalls = 0
        self.totaltime = 0.0
        self.log_level = log_level
        self.timer = timeit.default_timer
        self.formatter = formatter

    def __call__(self, *args: Any, **kw: Any) -> None:
        """Profile a singe call to the function."""
        fn = self.fn
        timer = self.timer
        self.ncalls += 1
        try:
            start = timer()
            return fn(*args, **kw)
        finally:
            duration = timer() - start
            self.totaltime += duration
            funcname = fn.__name__
            filename = fn.__code__.co_filename
            lineno = fn.__code__.co_firstlineno

            logging.log(self.log_level, self.formatter("\n{file_name}->{fn_name}(...) ({duration:.3f}s)\n".format(
                file_name=os.path.basename(filename),
                fn_name=funcname,
                duration=duration
            )))
