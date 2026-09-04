from isa_utils.misc import *

from isa_utils import log
import time

def test_timeout():
    log.info("Testing call_with_timeout() case where timeout is reached.")
    test_func = lambda: time.sleep(1)
    try:
        call_with_timeout(func=test_func, timeout=0.1)
        log.error("Test failed; no exception was raised.")
    except Exception as exception:
        if isinstance(exception, TimeoutError):
            log.info("Test passed; caught a {}.", TimeoutError.__name__)
        else:
            log.error("Test failed; got a {} instead of a {}.", exception.__class__.__name__, TimeoutError.__name__)

def test_function_exception():
    log.info("Testing call_with_timeout() case where calling the function causes an exception.")
    test_func = lambda: 1/0
    try:
        call_with_timeout(func=test_func, timeout=0.1)
        log.error("Test failed; no exception was raised.")
    except Exception as exception:
        if isinstance(exception, ZeroDivisionError):
            log.info("Test passed; caught a {}.", ZeroDivisionError.__name__)
        else:
            log.error("Test failed; got a {} instead of a {}.", exception.__class__.__name__, ZeroDivisionError.__name__)

test_timeout()
test_function_exception()