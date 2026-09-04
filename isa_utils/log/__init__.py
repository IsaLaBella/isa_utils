# -*- coding: utf-8 -*-
"""
This module builds on the builtin logging module of Python.

Usage:
	A console logger and file logger are created by default. Additional loggers must be created using python's logging module, which will be used automatically.
	
	About unhandled exceptions:
		Unhandled exceptions will be automatically logged using existing loggers; there is no need to set up this functionality yourself.

	Functions:
		setup_logging():
			- Call this to setup logging.
			- If not called manually, is called automatically the first time a log call is made.
				- See function documentation for default settings.

		Use the following functions to write log messages with various levels (see individual functions for more information):
		- debug()
		- info()
		- warning()
		- error(); log_exception()
		- critical()
"""


import logging
import sys, pathlib
from typing import Dict, List, Any, Tuple
from threading import main_thread

from isa_utils.text.color.themes import THEME_STANDARD
from isa_utils.text import color, highlight_args, set_color_scheme, str_combine

# =============================================================================
# COLOR PARSING
# =============================================================================

set_color_scheme(THEME_STANDARD)

# =============================================================================
# THREADS
# =============================================================================

def rename_main_thread(name: str):
	"""
	Renames the main thread (default "Main") for logging purposes.

	Args:
		name (str): New name for the main thread.
	"""	
	main_thread().name = name

# =============================================================================
# LOGGING
# =============================================================================

loggers: List[logging.Logger] = []
__logging_enabled = False

# Monkey-patch the level "verbose" into the logging module.
logging.VERBOSE = 5
logging._levelToName[logging.VERBOSE] = 'VERBOSE'
logging._nameToLevel['VERBOSE'] = logging.VERBOSE


class __CustomFormatter(logging.Formatter):

	def __init__(self, do_color = True, *args, **kwargs):

		super().__init__(*args, **kwargs)
		self.do_color = do_color

		if do_color:
			global_format = str_combine(
				'[', color('{asctime:19.19}', 'time') , ']',
				'[', color('{module:<10.10}', 'module'), ':',
				color('{lineno:>4}', 'lineNo'), ']',
				# '[', color('{threadName:>6.6}', 'thread'), ']',
				# '{funcName}',
				' {message}',
			)

			self.level_formats = {
				logging.VERBOSE: str_combine(
					'[', color('{levelname:<5.5}', 'levelVerbose'), ']', global_format),
				logging.DEBUG: str_combine(
					'[', color('{levelname:<5.5}', 'levelDebug'), ']', global_format),
				logging.INFO: str_combine(
					'[', color('{levelname:<5.5}', 'levelInfo'), ']', global_format),
				logging.WARNING: str_combine(
					'[', color('{levelname:<5.5}', 'levelWarn'), ']', global_format),
				logging.ERROR: str_combine(
					'[', color('{levelname:<5.5}', 'levelError'), ']', global_format),
				logging.CRITICAL: str_combine(
					'[', color('{levelname:<5.5}', 'levelCrit'), ']', global_format),
			}

			self.level_colors = {
				logging.VERBOSE: 'messageVerbose',
				logging.DEBUG: 'messageDebug',
				logging.INFO: 'messageInfo',
				logging.WARNING: 'messageWarn',
				logging.ERROR: 'messageError',
				logging.CRITICAL: 'messageCrit',
			}
		
		else:
			global_format = str_combine(
				'[', '{asctime:19.19}', ']',
				'[', '{module:<10.10}', ':',
				'{lineno:>4}', ']',
				# '[', '{threadName:>6.6}', ']',
				# '{funcName}',
				' {message}',
			)
			
			self.level_formats = {
				logging.VERBOSE: str_combine(
					'[', '{levelname:<5.5}', ']', global_format),
				logging.DEBUG: str_combine(
					'[', '{levelname:<5.5}', ']', global_format),
				logging.INFO: str_combine(
					'[', '{levelname:<5.5}', ']', global_format),
				logging.WARNING: str_combine(
					'[', '{levelname:<5.5}', ']', global_format),
				logging.ERROR: str_combine(
					'[', '{levelname:<5.5}', ']', global_format),
				logging.CRITICAL: str_combine(
					'[', '{levelname:<5.5}', ']', global_format),
			}

			self.level_colors = {
				logging.VERBOSE: 'none',
				logging.DEBUG: 'none',
				logging.INFO: 'none',
				logging.WARNING: 'none',
				logging.ERROR: 'none',
				logging.CRITICAL: 'none',
			}

		self.level_formatters = {
			level: logging.Formatter(level_format, style='{')
			for level, level_format in self.level_formats.items()
		}

	def format(self, record):

		if self.do_color:
			record.msg = color(record.msg, self.level_colors.get(record.levelno))

		formatter = self.level_formatters.get(record.levelno)
		return formatter.format(record)


def __setup_logger(name: str, level=logging.DEBUG, **kwargs) -> logging.Logger:

	handler = kwargs.get('handler', logging.StreamHandler())
	formatter = kwargs.get('formatter', logging.Formatter())
	addToLoggerList = kwargs.get('addToLoggerList', True)

	logger = logging.getLogger(name)
	logger.setLevel(level)
	logger.propagate = False

	__clear_handlers(logger)
	handler.setFormatter(formatter)
	logger.addHandler(handler)

	global loggers
	if addToLoggerList:
		if logger not in loggers:
			loggers.append(logger)

	return logger


def __clear_handlers(logger: logging.Logger):

	while len(logger.handlers) > 0:

		logger.removeHandler(logger.handlers[0])


def __print_log_head(level: int):

	levelToName = logging._levelToName
	excluded = [logging.NOTSET]
	levels = {level: levelToName[level]
			  for level in levelToName if level not in excluded}

	simpleLogger = __setup_logger('simple', addToLoggerList=False,
								 formatter=logging.Formatter(
									 '{message:^90}', style='{')
								 )

	simpleLogger.info('=' * 90)
	simpleLogger.info(
		'Logging has been set up with level \'{}\' ({}).'.format(
			logging._levelToName[level], level)
	)
	simpleLogger.info('Log messages will appear as follows:')
	simpleLogger.info('-' * 90)

	# Constructing the record and handling directly via the logger
	# bypasses the log level setting and enables modification of
	# record fields for demonstration purposes.
	def makeDemoRecord(level, msg):

		record = logging.LogRecord(
			name=__consoleLogger.name,
			level=level,
			pathname='Module',
			lineno='Line',
			msg=msg,
			args=(),
			exc_info=None,)

		record.threadName = 'Thread'

		return record

	def demoMSG(level, msg): __consoleLogger.handle(makeDemoRecord(level, msg))

	for level in levels:

		levelName = levels[level]
		msg = 'This is a(n) {} (log level {}) message [{}].'

		if __consoleLogger.isEnabledFor(level):
			msg = highlight_args(msg, levelName, level, 'ENABLED')
		else:
			msg = highlight_args(msg, levelName, level, 'NOT ENABLED')

		demoMSG(level, msg)

	simpleLogger.info('=' * 90)
	simpleLogger.info('--- BEGINNING OF LOG ---')
	simpleLogger.info('=' * 90)


def __print_log_tail():

	simpleLogger = logging.getLogger('simple')

	simpleLogger.info('=' * 90)
	simpleLogger.info('--- END OF LOG ---')
	simpleLogger.info('=' * 90)


def setup_logging(
		level=logging.DEBUG,
		*,
		encoding='utf-8',
		log_file_name = None,
		overwrite_file: bool = True,
		color_scheme: Dict[str, Tuple[int, int, int]] = THEME_STANDARD
	):

	"""
	Initialises loggers. Called automatically if loggers have not already been set up.

	Args:
		level (int, optional): Logging level to use. Defaults to logging.DEBUG (10).

		**kwargs:
			encoding (str) - text encoding for the log file. Default: 'utf-8'
			logFile (str) - path/name of the log file. Default (if None): name of the main script.
			overwriteFile (bool) - whether to overwrite the existing log file. Default: True.
			color_scheme (Dict[str, Tuple[int, int, int]]) - color scheme to use for logging. Default: THEME_STANDARD.
	"""
	
	global __logging_enabled
	if __logging_enabled: return

	set_color_scheme(color_scheme)

	fileMode = 'w' if overwrite_file else 'a'

	if log_file_name == None:
		import os
		scriptName = os.path.basename(sys.argv[0]).rsplit('.',1)[0]
		log_file_name = '{}.log'.format(scriptName)

	global __consoleLogger
	__consoleLogger = __setup_logger(
		'console', level, formatter=__CustomFormatter())
	
	global __fileLogger
	__fileLogger = __setup_logger(
		'file', level,
		handler=logging.FileHandler(log_file_name, fileMode, encoding=encoding),
		formatter=__CustomFormatter(do_color=False)
	)

	# Set up automatic exception logging
	def _log_exception(exc_type, exc_value, exc_traceback):
		if issubclass(exc_type, KeyboardInterrupt):
			sys.__excepthook__(exc_type, exc_value, exc_traceback)
			return

		error("Program ended with unhandled exception:", exc_info=(exc_type, exc_value, exc_traceback),
			  stacklevel = __STACKLEVEL + 2)
		conclude_logging()
	
	sys.excepthook = _log_exception

	# __printLogHead(level)

	__logging_enabled = True

	info("Log file opened: {}.", str(pathlib.Path(log_file_name).resolve()),
		 stacklevel = __STACKLEVEL + 1)


def conclude_logging():
	"""
	Disables existing loggers handling log calls via this module only.
	IMPORTANT: 
		Although the loggers will no longer handle messages, they still exist in memory within the builtin logging module.
		Therefore, repeated use of concludeLogging() and setupLogging() in the same script will lead to memory leaks.
	"""
	#__printLogTail()

	global loggers
	for logger in loggers:
		loggers.remove(logger)
		logger.disabled = True

	global __logging_enabled
	__logging_enabled = False


__STACKLEVEL = 3

def verbose(msg: str, *args: Any, **kwargs):
	"""
	Log a verbose message (log level = 5) to all loggers.
	Has built-in string.format() functionality. See below.

	Args:
		msg (str): The message to log.
			msg.format(*args) is called automatically before the message is logged.
			Format arguments specified this way are automatically highlighted using a different color in the log.
		*args (Any): format arguments for msg.
	"""	
	__log(logging.VERBOSE, msg, *args, **kwargs)


def debug(msg: str, *args: Any, **kwargs):
	"""
	Log a debug message (log level = 10) to all loggers.
	Has built-in string.format() functionality. See below.

	Args:
		msg (str): The message to log.
			msg.format(*args) is called automatically before the message is logged.
			Format arguments specified this way are automatically highlighted using a different color in the log.
		*args (Any): format arguments for msg.
	"""	
	__log(logging.DEBUG, msg, *args, **kwargs)


def info(msg: str, *args: Any, **kwargs):
	"""
	Log an info message (log level = 20) to all loggers.
	Has built-in string.format() functionality. See below.

	Args:
		msg (str): The message to log.
			msg.format(*args) is called automatically before the message is logged.
			Format arguments specified this way are automatically highlighted using a different color in the log.
		*args (Any): format arguments for msg.
	"""	
	__log(logging.INFO, msg, *args, **kwargs)


def warning(msg: str, *args: Any, **kwargs):
	"""
	Log an warning message (log level = 30) to all loggers.
	Has built-in string.format() functionality. See below.

	Args:
		msg (str): The message to log.
			msg.format(*args) is called automatically before the message is logged.
			Format arguments specified this way are automatically highlighted using a different color in the log.
		*args (Any): format arguments for msg.
	""" 
	__log(logging.WARNING, msg, *args, **kwargs)


def error(msg: str, *args: Any, **kwargs):
	"""
	Log an error message (log level = 40) to all loggers. 
	Does NOT raise exceptions.
	Has built-in string.format() functionality. See below.

	Args:
		msg (str): The message to log.
			msg.format(*args) is called automatically before the message is logged.
			Format arguments specified this way are automatically highlighted using a different color in the log.
		*args (Any): format arguments for msg.
	""" 
	__log(logging.ERROR, msg, *args, **kwargs)

def log_exception(msg: str, *args: Any, **kwargs):
	"""
	Call error(msg, *args, **kwargs, exc_info = True), then sys.exit(-1).
	Functions like raising an unhandled exception.

	Args:
		msg (str): The message to log.
			msg.format(*args) is called automatically before the message is logged.
			Format arguments specified this way are automatically highlighted using a different color in the log.
		*args (Any): format arguments for msg.
	""" 
	error(msg, *args, **kwargs, exc_info = True)
	sys.exit(-1)


def critical(msg: str, *args: Any, **kwargs):
	"""
	Log a critical message (log level = 50) to all loggers. 
	Does NOT raise exceptions.
	Has built-in string.format() functionality. See below.

	Args:
		msg (str): The message to log.
			msg.format(*args) is called automatically before the message is logged.
			Format arguments specified this way are automatically highlighted using a different color in the log.
		*args (Any): format arguments for msg.
	""" 
	__log(logging.CRITICAL, msg, *args, **kwargs)


def __log(level: int, msg: str, *args: Any, **kwargs):

	if not __logging_enabled:
		setup_logging()

	msg = str(msg)

	kwargs['stacklevel'] = kwargs.get('stacklevel', __STACKLEVEL) # NYI in Python 3.6.8 :c

	for logger in loggers:
		if logger.handlers[0].formatter.do_color: # Loggers will only have 1 handler if setup through this module.
			logger.log(level, highlight_args(msg, *args), **kwargs)
		else:
			logger.log(level, msg.format(*args), **kwargs)