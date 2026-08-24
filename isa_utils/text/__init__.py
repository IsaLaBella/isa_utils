# -*- coding: utf-8 -*-

from typing import Any, Dict, List
from typing import Sequence, Tuple
import inspect

from isa_utils.text.color.base import ANSI_RGB, BASE_COLORS
from isa_utils.text.color.themes import THEME_NONE
from isa_utils.text.color.base import ANSI_RESET

# ============================================================================ #
#                                    Colors                                    #
# ============================================================================ #

# ================================= Constants ================================ #

COLOR_SCHEME = THEME_NONE

COLORS = {**BASE_COLORS, **COLOR_SCHEME}

# ================================= Functions ================================ #

def set_color_scheme(colorScheme: Dict[str, Tuple[int, int, int]]):
	"""
	Set the color scheme used to obtain color values from given keys.

	Args:
		colorScheme (Dict[str, Tuple[int, int, int]]): Color scheme to change to. See constants.py for options.
	"""	

	global COLORS
	COLORS = {**BASE_COLORS, **colorScheme}


def get_color_scheme() -> Dict[str, Tuple[int, int, int]]:
	"""
	Get the color scheme used to obtain color values from given keys.

	Returns:
		Dict[str, Tuple[int, int, int]]: The current active color scheme.
	"""	

	global COLORS
	return COLORS


def rgb_to_ansi(r: int, g: int, b: int):
	"""
	Converts the given r, g and b color values (from 0 to 255) into an ANSI escape sequence.

	Args:
		r (int): Red value. Clamped between 0 and 255.
		g (int): Green value. Clamped between 0 and 255.
		b (int): Blue value. Clamped between 0 and 255.

	Returns:
		_type_: ANSI escape sequence representing the given r, g and b values.
	"""	

	r = min(max(r, 0), 255)
	g = min(max(g, 0), 255)
	b = min(max(b, 0), 255)
	return ANSI_RGB.format(r, g, b)


# TODO implement terminal color type support: 'none,' and others
def color(text: str, colorName: str, terminalColorSupport: str = 'ansii') -> str:
	"""
	Colors the given text by adding ANSI escape sequences.

	Args:
		text (str): Text to color.
		colorName (str): Desired color of the text. Must be a key in the current color scheme.
		terminalColorSupport (str, optional): NYI. What kind of coloring scheme is supported by the terminal. Defaults to 'ansii'.

	Raises:
		ValueError: If the given color is the same as the ansi reset sequence.

	Returns:
		str: Colored input string.
	"""	

	global COLORS

	color = COLORS[colorName]
	reset = ANSI_RESET

	if color == reset:
		raise ValueError('Color cannot be the same sequence as reset!')

	if color == COLORS['none']:
		return text

	color = rgb_to_ansi(*color)

	text = parse_nested_colors(text, color)

	output = color + text + reset
	return output


def parse_nested_colors(text: str, ansiColor: str) -> str:
	"""
	Replaces ansiReset in the given string with the given color.

	Used to correct: '{color1} some text {color2} more text {colorReset} and more {colorReset}.'
	to: '{color1} some text {color2} more text {color1} and more {colorReset}.'

	Args:
		text (str): Input text to process.
		ansiColor (str): Color to replace the ansi color reset escape sequence with.

	Raises:
		ValueError: If the given color is the same as the ansi reset sequence.

	Returns:
		str: Recolored input string.
	"""	

	global COLORS

	color = ansiColor
	reset = ANSI_RESET

	if color == reset:
		raise ValueError('Color cannot be the same sequence as reset!')

	while reset in text:
		indexStart = text.index(reset)
		indexEnd = indexStart + len(reset)
		text = text[:indexStart] + color + text[indexEnd:]

	return text


def color_args(text: str, *args: Tuple[object, str]) -> str:
	"""
	Colors each of the provided arguments using ANSI escape sequences, then calls .format() on the input text using the colored arguments.

	Args:
		text (str): Input text. Must be a string whose format() method can be called with the given arguments.
		*args (Tuple[object, str]): Pairs of objects and colors to format them with.

	Raises:
		TypeError: If 'text' is not a string.

	Returns:
		str: Formatted string with format arguments colored using ANSI escape sequences.
	"""	

	global COLORS

	if not issubclass(type(text), str):
		raise TypeError("Argument 'text' must be an instance of str, not '{}'.".format(type(text)))
	
	formatArgs = []

	for arg in args:

		argString = str(arg[0])
		argColorName = arg[1]
		formatArgs.append(color(argString, argColorName))

	return text.format(*formatArgs)


def highlight_args(text: str, *args: Any) -> str:
	"""
	Calls color_args() using the color 'highlight' in the current color scheme.

	Args:
		text (str): Input text. Must be a string whose format() method can be called with the given arguments.
		*args (Any): Arguments with which to call .format() on the input text.

	Returns:
		str: Formatted string with format arguments highlighted using ANSI escape sequences.
	"""	

	args = [(arg, 'highlight') for arg in args]
	return color_args(text, *args)

# =============================================================================
# %% FORMATTING
# =============================================================================


def split_leading_whitespace(text: str):
	'''
	Separates any leading whitespace from a line and returns both the leading
	whitespace and the remainder of the line.
	'''

	leadingWhitespace = len(text) - len(text.lstrip())
	line = text[leadingWhitespace:]
	leadingWhitespace = text[:leadingWhitespace]

	return leadingWhitespace, line


def line_wrap(text: str, lineLength: int = 80):
	'''
	Wraps the given text with the provided line length. Leading white space is
	preserved, while trailing whitespace is removed. Lines shorter than the limit
	are not affected.
	'''

	newLineDelimiters = ('-', '\n')

	lines = text.split('\n')
	lines = [line.rstrip() for line in lines]  # Remove trailing whitespace

	lineIndex = 0
	while lineIndex < len(lines):

		line = lines[lineIndex]
		leadingWhitespace, line = split_leading_whitespace(line)

		# Ignore empty lines.
		if len(line) == 0:
			lineIndex += 1
			continue

		if len(line) > lineLength:

			# Find end of last word.
			lineEnd = line[:lineLength].rfind(' ')
			if lineEnd == -1:
				lineEnd = lineLength

			trimmedLine = line[:lineEnd]
			remainder = line[lineEnd:] + ' '
			if remainder[0] == ' ':
				remainder = remainder[1:]

			lines[lineIndex] = leadingWhitespace + trimmedLine

			if lineIndex < len(lines) - 1:
				nextLine = lines[lineIndex + 1]
				nextLeadingWhitespace, nextLine = split_leading_whitespace(
					nextLine)

				if (not len(nextLine) == 0 and leadingWhitespace == nextLeadingWhitespace and
						not nextLine.startswith(newLineDelimiters)):
					lines[lineIndex + 1] = leadingWhitespace + \
						remainder + nextLine

				else:
					if line.startswith(newLineDelimiters):
						for delimiter in newLineDelimiters:
							if line.startswith(delimiter):
								break
						leadingWhitespace += ' ' * len(delimiter)
						leadingWhitespace += split_leading_whitespace(
							line[len(delimiter):])[0]

					lines.insert(lineIndex + 1, leadingWhitespace + remainder)
			else:
				lines.append(leadingWhitespace + remainder)

		lineIndex += 1

	# Verify. Print warning if some lines are still too long.
	if any([len(line.lstrip()) > lineLength for line in lines]):

		from log import error  # analysis:ignore
		error('Check implementation of {}.{}()! Some lines are still too long!',
			  __name__, inspect.stack()[0][3])
		error('Bad lines: ')
		badLines = [line for line in lines if len(line) > lineLength]
		for line in badLines:
			error('\t\'{}\' (length {} > {})',
				  line, len(line.lstrip()), lineLength)

	return '\n'.join(lines)


def str_combine(*strings: str, **kwargs) -> str:
	'''
	Slightly more readable/easily codeable way of combining a list of strings.

	For if you don't want to use a multiline string for some reason.
	'''

	seperator = kwargs.get('sep', kwargs.get('seperator', ''))

	return seperator.join(strings)

# TODO complete


def format_dict(_dict: dict, **kwargs) -> Tuple[str, List[Any]]:
	'''
	Generates a format string and argument list for a given dictionary.

	Example usage:

		some_dict = {'foo': 1, 'bar': 2, 'baz': 3}

		formatString, formatArgs = formatDict(some_dict)

		print(('{}\'s dictionary: ' + formatString + '. It has {} elements!').format('A cool person', *formatArgs, len(some_dict)))

	   # prints => A cool person's dictionary: foo: 1, bar: 2, baz: 3. It has 3 elements!
	'''

	seperator = kwargs.get('sep', kwargs.get('seperator', ', '))
	dictFormat = kwargs.get('dictFormat', '{}: {}')

	formatString = seperator.join([dictFormat] * len(_dict))
	formatArgs = tuple([item for key, value in _dict.items()
					   for item in (key, value)])

	return formatString, formatArgs


def format_sequence(_sequence: Sequence, *, seperator = ', ', listFormat = '{}') -> str:
	'''
	Generates a format string a given sequence.

	Example usage:

		some_sequence = [1, 2, 3]

		formatString = formatSequence(some_sequence)

		print(('{}\'s sequence: ' + formatString + '. It has {} elements!').format('A cool person', *some_sequence, len(some_sequence)))

	   # prints => A cool person's sequence: 1, 2, 3. It has 3 elements!
	'''

	formatString = seperator.join([listFormat] * len(_sequence))

	return formatString


# =============================================================================
# %% MAIN PROGRAM
# =============================================================================

def main():

	from log import setup_logging, conclude_logging
	setup_logging()

	conclude_logging()

if __name__ == '__main__':

	main()
