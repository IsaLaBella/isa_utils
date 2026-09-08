"""
Submodule that implements a basic color class.
"""

# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #

from typing import Any, Tuple, TypeAlias
from enum import Enum, auto

# ---------------------------------------------------------------------------- #
#                               Helper Functions                               #
# ---------------------------------------------------------------------------- #

def _clamp(value: float | int, min_value: float | int, max_value: float | int) -> float | int:
    return min(max_value, max(min_value, value))

def _float_to_8_bit_unsigned(value: float, min_float_value: float = 0, max_float_value: float = 1) -> int:
    new_value = value*(255-0)/(max_float_value - min_float_value)
    return int(_clamp(new_value, 0, 255))

def _8_bit_unsigned_to_float(value: int, min_float_value: float = 0, max_float_value: float = 1) -> float:
    value = _clamp(value, 0, 255)
    return value*(max_float_value - min_float_value)/(255-0)
     
# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #

class COLOR_MODE(Enum):

    FLOAT_0_TO_1 = auto()
    UINT8 = auto()

class Color():

    __MAX_FLOAT_VAL = 1
    __MIN_FLOAT_VAL = 0

    def __init__(self, *args, **kwargs):

        # Defaults
        self.__r = 0
        self.__g = 0
        self.__b = 0

        self.color_mode = kwargs.get("color_mode", COLOR_MODE.FLOAT_0_TO_1)

        match len(args):
            case 0:
                self.r = self.g = self.b = 0
            case 1:
                self.r = self.g = self.b = args[0]
            case 3:
                self.r = args[0]
                self.g = args[1]
                self.b = args[2]
            case _:
                raise ValueError(f"Incorrect number of wildcard arguments. Must be 0, 1 or 3, not {len(args)}")

        self.r = kwargs.get("r", self.r)
        self.g = kwargs.get("g", self.g)
        self.b = kwargs.get("b", self.b)

        # self.r_8bit = kwargs.get("r_8bit", self.r_8bit)
        # self.g_8bit = kwargs.get("g_8bit", self.g_8bit)
        # self.b_8bit = kwargs.get("b_8bit", self.b_8bit)

    # -------------------------- Properties: Color Mode -------------------------- #

    def __get_color_mode(self) -> COLOR_MODE:
        return self.__color_mode

    def __set_color_mode(self, color_mode: COLOR_MODE) -> None:

        if not isinstance(color_mode, COLOR_MODE):
            raise TypeError(f"Invalid type for color_mode (must be {COLOR_MODE.__name__} or {COLOR_MODE.__class__.__name__}, not {type(color_mode).__name__})")
        
        if color_mode not in COLOR_MODE:
            raise ValueError(f"Invalid value for color mode: {color_mode}.")
        
        self.__color_mode = color_mode

    color_mode = property(__get_color_mode, __set_color_mode)

    # --------------------- Properties: r, g and b as floats --------------------- #
    
    def __get_r_float(self) -> float:
        return self.__r

    def __set_r_float(self, value: float):
        self.__r = _clamp(value, self.__MIN_FLOAT_VAL, self.__MAX_FLOAT_VAL)

    def __get_g_float(self) -> float:
            return self.__g
    
    def __set_g_float(self, value: float):
        self.__g = _clamp(value, self.__MIN_FLOAT_VAL, self.__MAX_FLOAT_VAL)

    def __get_b_float(self) -> float:
            return self.__b
    
    def __set_b_float(self, value: float):
        self.__b = _clamp(value, self.__MIN_FLOAT_VAL, self.__MAX_FLOAT_VAL)

    r_float = property(__get_r_float, __set_r_float)
    g_float = property(__get_g_float, __set_g_float)
    b_float = property(__get_b_float, __set_b_float)

    @property
    def rgb_float(self) -> Tuple[float, float, float]:
        return (self.r_float, self.g_float, self.b_float)

    # -------------- Properties: r, g and b as 8-bit unsigned values ------------- #
    
    def __get_r_8bit(self) -> int:
        return _float_to_8_bit_unsigned(self.__r)
    
    def __set_r_8bit(self, value: int):
        self.__r = _8_bit_unsigned_to_float(value, self.__MIN_FLOAT_VAL, self.__MAX_FLOAT_VAL)

    def __get_g_8bit(self) -> int:
        return _float_to_8_bit_unsigned(self.__g)
    
    def __set_g_8bit(self, value: int):
        self.__g = _8_bit_unsigned_to_float(value, self.__MIN_FLOAT_VAL, self.__MAX_FLOAT_VAL)

    def __get_b_8bit(self) -> int:
        return _float_to_8_bit_unsigned(self.__b)
    
    def __set_b_8bit(self, value: int):
        self.__b = _8_bit_unsigned_to_float(value, self.__MIN_FLOAT_VAL, self.__MAX_FLOAT_VAL)

    r_8bit = property(__get_r_8bit, __set_r_8bit)
    g_8bit = property(__get_g_8bit, __set_g_8bit)
    b_8bit = property(__get_b_8bit, __set_b_8bit)

    @property
    def rgb_24bit(self) -> Tuple[int, int, int]:
        return (self.r_8bit, self.g_8bit, self.b_8bit)

    # ---------------- Properties: r, g and b based on color mode ---------------- #

    def __get_r(self) -> float | int:

        match self.color_mode:
            case COLOR_MODE.FLOAT_0_TO_1:
                return self.r_float
            case COLOR_MODE.UINT8:
                return self.r_8bit
            case _:
                raise ValueError(f"{self.__class__.__name__} has invalid or not implemented value for color_mode ({self.color_mode}).")

    def __set_r(self, value: float | int):
        
        match self.color_mode:
            case COLOR_MODE.FLOAT_0_TO_1:
                self.r_float = value
            case COLOR_MODE.UINT8:
                self.r_8bit = value
            case _:
                raise ValueError(f"{self.__class__.__name__} has invalid or not implemented value for color_mode ({self.color_mode}).")

    def __get_g(self) -> float:

        match self.color_mode:
            case COLOR_MODE.FLOAT_0_TO_1:
                return self.g_float
            case COLOR_MODE.UINT8:
                return self.g_8bit
            case _:
                raise ValueError(f"{self.__class__.__name__} has invalid or not implemented value for color_mode ({self.color_mode}).")
    
    def __set_g(self, value: float | int):
        
        match self.color_mode:
            case COLOR_MODE.FLOAT_0_TO_1:
                self.g_float = value
            case COLOR_MODE.UINT8:
                self.g_8bit = value
            case _:
                raise ValueError(f"{self.__class__.__name__} has invalid or not implemented value for color_mode ({self.color_mode}).")

    def __get_b(self) -> float:

        match self.color_mode:
            case COLOR_MODE.FLOAT_0_TO_1:
                return self.b_float
            case COLOR_MODE.UINT8:
                return self.b_8bit
            case _:
                raise ValueError(f"{self.__class__.__name__} has invalid or not implemented value for color_mode ({self.color_mode}).")
    
    def __set_b(self, value: float | int):
        
        match self.color_mode:
            case COLOR_MODE.FLOAT_0_TO_1:
                self.b_float = value
            case COLOR_MODE.UINT8:
                self.b_8bit = value
            case _:
                raise ValueError(f"{self.__class__.__name__} has invalid or not implemented value for color_mode ({self.color_mode}).")

    r = property(__get_r, __set_r)
    g = property(__get_g, __set_g)
    b = property(__get_b, __set_b)

    @property
    def rgb(self) -> Tuple[float | int, float | int, float | int]:
        return (self.r, self.g, self.b)

    # ----------------------------------- Other ---------------------------------- #

    def __repr__(self) -> str:
        return f"<Color object: {self.r}, {self.g}, {self.b}>"

    def __str__(self) -> str:
        return f"(r={self.r}, g={self.g}, b={self.b})"