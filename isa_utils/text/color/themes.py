# -*- coding: utf-8 -*-

# =============================================================================
# %% IMPORTS
# =============================================================================

from typing import Dict
from typing import Tuple

from isa_utils.text.color.base import BASE_COLORS

THEME_NONE: Dict[str, Tuple[int, int, int]] = {
	'levelVerbose': BASE_COLORS['none'],
	'levelDebug': BASE_COLORS['none'],
	'levelInfo': BASE_COLORS['none'],
	'levelWarn': BASE_COLORS['none'],
	'levelError': BASE_COLORS['none'],
	'levelCrit': BASE_COLORS['none'],

	'messageVerbose': BASE_COLORS['none'],
	'messageDebug': BASE_COLORS['none'],
	'messageInfo': BASE_COLORS['none'],
	'messageWarn': BASE_COLORS['none'],
	'messageError': BASE_COLORS['none'],
	'messageCrit': BASE_COLORS['none'],

	'highlight': BASE_COLORS['none'],
	'time': BASE_COLORS['none'],
	'module': BASE_COLORS['none'],
	'thread': BASE_COLORS['none'],
	'lineNo': BASE_COLORS['none']
}

THEME_STANDARD: Dict[str, Tuple[int, int, int]] = {
	'levelVerbose': BASE_COLORS['cSoftCyan'],
	'levelDebug': BASE_COLORS['cSoftBlue'],
	'levelInfo': BASE_COLORS['cSoftGreen'],
	'levelWarn': BASE_COLORS['cSoftYellow'],
	'levelError': BASE_COLORS['cSoftRed'],
	'levelCrit': BASE_COLORS['cBrightRed'],

	'messageVerbose': BASE_COLORS['cSoftCyan'],
	'messageDebug': BASE_COLORS['cSoftBlue'],
	'messageInfo': BASE_COLORS['cSoftGreen'],
	'messageWarn': BASE_COLORS['cSoftYellow'],
	'messageError': BASE_COLORS['cSoftRed'],
	'messageCrit': BASE_COLORS['cBrightRed'],

	'highlight': BASE_COLORS['cWhite'],
	'time': BASE_COLORS['cLightGrey'],
	'module': BASE_COLORS['cLightGrey'],
	'thread': BASE_COLORS['cLightGrey'],
	'lineNo': BASE_COLORS['cLightGrey']
}

THEME_SPOOKY_GORL: Dict[str, Tuple[int, int, int]] = {
	'levelVerbose': BASE_COLORS['cSoftMagenta'],
	'levelDebug': BASE_COLORS['cSoftMagenta'],
	'levelInfo': BASE_COLORS['cSoftCyan'],
	'levelWarn': BASE_COLORS['cPastelToxicGreen'],
	'levelError': BASE_COLORS['cHotPink'],
	'levelCrit': BASE_COLORS['cBrightMagenta'],

	'messageVerbose': BASE_COLORS['cPaintPink'],
	'messageDebug': BASE_COLORS['cPaintPink'],
	'messageInfo': BASE_COLORS['none'],
	'messageWarn': BASE_COLORS['cPastelToxicGreen'],
	'messageError': BASE_COLORS['cHotPink'],
	'messageCrit': BASE_COLORS['cBrightMagenta'],

	'highlight': BASE_COLORS['cEctoplasm'],
	'time': BASE_COLORS['none'],
	'module': BASE_COLORS['none'],
	'thread': BASE_COLORS['cSoftCyan'],
	'lineNo': BASE_COLORS['cEctoplasm']
}