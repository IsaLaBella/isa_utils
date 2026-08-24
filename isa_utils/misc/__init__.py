import sys, pathlib
import threading
from typing import Any, Callable, Dict, Iterable
if __name__ =='__main__': sys.path.append(str(pathlib.Path(__file__).parent.parent.resolve()))

def enforce_argument_type(arg: object, argname: str, type_: type):
	"""
	Raises a TypeError if the given object is not of the given type.
	The check is performed by calling isinstance(arg, type_). Thus, a TypeError will not be raised if, for example, 'arg' is a list, but 'type_' is 'typing.Sequence'.

	Args:
		arg (object): Object to check the type of.
		argname (str): Name of the given argument. This is used to generate the resulting error message.
		type_ (type): Type that arg must be an instance of.

	Raises:
		TypeError: If the given object is not an instance of the given type.
	"""	

	if not isinstance(arg, type_):
		raise TypeError("Argument '{}' must be of type {}, not {}.".format(argname, type_.__name__, arg.__class__.__name__))

def call_with_timeout(
		func: Callable,
		func_args: Iterable[Any] = (),
		func_kwargs: Dict[str, Any] = {},
		timeout: int|None = None,
		error_message_on_timeout: str = "Timed out while waiting for function."
	) -> Any:
	"""
	Calls the given function with a timeout, even if the original function lacks a timeout.

	This is useful for blocking function calls that normally lack a timeout, such as socket.socket().recv(), where timeout is specified at socket instantiation rather than at function call.

	Args:
		func (Callable): Function to call.
		func_args (Iterable[Any], optional): Positional/wildcard arguments to call the function with. Defaults to an empty tuple.
		func_kwargs (Dict[str, Any], optional): Keyword arguments to call the function with. Defaults to an empty dict.
		timeout (int | None, optional): Maximum allowable time for the function call to take, in seconds. If None, then no timeout is enforced. Defaults to None.
		error_message_on_timeout (str, optional): Error message to include in the TimeoutError raised if and when the timeout is reached. Defaults to "Timed out while waiting for function.".

	Raises:
		TimeoutError: if the given timeout is reached before the function call finishes.

	Returns:
		Any: whatever the provided function returns.
	"""	

	ret_container = []
	def thread_target():
		try:
			ret_val = func(*func_args, **func_kwargs)
		except Exception as exception:
			ret_container.append(exception)
			return

		ret_container.append(ret_val)

	thread = threading.Thread(target = thread_target, daemon=True)
	thread.start()
	thread.join(timeout=timeout)

	if thread.is_alive():
		raise TimeoutError(error_message_on_timeout)
	
	ret_val = ret_container[0]
	if isinstance(ret_val, Exception):
		raise ret_val.__class__("Call of function {} with timeout failed due to an exception.".format(func.__name__)) from ret_val
	return ret_val

if __name__ == "__main__":
	
	from prodtest_utils import log
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