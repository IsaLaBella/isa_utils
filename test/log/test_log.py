from isa_utils.log import *

setup_logging(level = logging.VERBOSE)

verbose("This is a verbose message.")
debug("This is a debug message.")
info("This is an info message.")
warning("This is a warning.")
error("This is an error message.")
critical("This is a critical message.")

conclude_logging()