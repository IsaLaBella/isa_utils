# =============================================================================
# %% COLORS
# =============================================================================
from typing import Dict, Tuple


ANSI_RGB = '\x1b[38;2;{0};{1};{2}m'
ANSI_RESET = '\x1b[0m'
BASE_COLORS: Dict[str, Tuple[int, int, int]] = {
    'none': (-1, -1, -1),

    'cBlack': (0, 0, 0),
    'cDarkGrey': (100, 100, 100),
    'cLightGrey': (200, 200, 200),
    'cWhite': (255, 255, 255),

    'cRed': (200, 0, 0),
    'cGreen': (0, 200, 0),
    'cBlue': (0, 0, 200),
    'cCyan': (0, 200, 200),
    'cMagenta': (200, 0, 200),
    'cYellow': (200, 200, 0),

    'cSoftRed': (200, 100, 100),
    'cSoftGreen': (100, 200, 100),
    'cSoftBlue': (100, 100, 200),
    'cSoftCyan': (100, 200, 200),
    'cSoftMagenta': (200, 100, 200),
    'cSoftYellow': (200, 200, 100),

    'cBrightRed': (255, 0, 0),
    'cBrightGreen': (0, 255, 0),
    'cBrightBlue': (0, 0, 255),
    'cBrightCyan': (0, 255, 255),
    'cBrightMagenta': (255, 0, 255),
    'cBrightYellow': (255, 255, 0),

    'cPastelToxicGreen': (128, 250, 120),
    'cEctoplasm': (75, 255, 215),
    'cLime': (125, 225, 0),
    'cSoftLime': (125, 225, 75),
    'cHotPink': (255, 105, 180),
    'cCottonCandyPink': (221, 186, 229),
    'cPaintPink': (195, 162, 199),
    'cGrape': (27, 14, 30),
    'cPuce': (78, 22, 9),
}