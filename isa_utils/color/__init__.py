"""
Submodule that implements a basic color class.
"""

# ---------------------------------------------------------------------------- #
#                                    Imports                                   #
# ---------------------------------------------------------------------------- #

from typing import Any, Tuple, TypeAlias
from enum import Enum, auto
     
# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #

class COLOR_MODE(Enum):

    FLOAT_0_TO_1 = auto()
    UINT8 = auto()

class Color():

    __MAX_RGB_FLOAT_VAL = 1
    __MIN_RGB_FLOAT_VAL = 0

    __MIN_RGB_UINT8_VAL = 0
    __MAX_RGB_UINT8_VAL = 255

    def __init__(self, *args, **kwargs):

        # Defaults
        self.__r = 0.0
        self.__g = 0.0
        self.__b = 0.0

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

        # Try to convert to enum type. No explicit type/value checking needed - calling COLOR_MODE(color_mode) does it already.
        self.__color_mode = COLOR_MODE(color_mode)

    color_mode = property(__get_color_mode, __set_color_mode)

    # --------------------- Properties: r, g and b as floats --------------------- #

    @classmethod
    def __check_rgb_float_value(cls, value: float) -> float:
        try:
            value = float(value) # Converting to float before comparison raises more sensible type errors for invalid types (i.e. 'could not convert x to float' instead of 'cannot compare float to x')
        except ValueError:
            raise TypeError(f"Invalid type for float value of rgb channel. Must be float or convertible to float.")
        
        if value > cls.__MAX_RGB_FLOAT_VAL or value < cls.__MIN_RGB_FLOAT_VAL:
            raise ValueError(f"Invalid float value for rgb channel of {cls.__name__}. Must be between {cls.__MIN_RGB_FLOAT_VAL} and {cls.__MAX_RGB_FLOAT_VAL}.")

        return value
    
    def __get_r_float(self) -> float:
        return self.__r

    def __set_r_float(self, value: float):
        self.__r = self.__check_rgb_float_value(value)

    def __get_g_float(self) -> float:
        return self.__g
    
    def __set_g_float(self, value: float):
        self.__g = self.__check_rgb_float_value(value)

    def __get_b_float(self) -> float:
        return self.__b
    
    def __set_b_float(self, value: float):
        self.__b = self.__check_rgb_float_value(value)

    r_float = property(__get_r_float, __set_r_float)
    g_float = property(__get_g_float, __set_g_float)
    b_float = property(__get_b_float, __set_b_float)

    @property
    def rgb_float(self) -> Tuple[float, float, float]:
        return (self.r_float, self.g_float, self.b_float)

    # -------------- Properties: r, g and b as 8-bit unsigned values ------------- #

    @classmethod
    def __check_rgb_uint8_value(cls, value: int) -> int:
        try:
            value = int(value) # Converting to int before comparison raises more sensible type errors for invalid types (i.e. 'could not convert x to int' instead of 'cannot compare int to x')
        except ValueError:
            raise TypeError(f"Invalid type for uint8 value of rgb channel. Must be int or convertible to int.")
        
        if value > cls.__MAX_RGB_UINT8_VAL or value < cls.__MIN_RGB_UINT8_VAL:
            raise ValueError(f"Invalid uint8 value for rgb channel of {cls.__name__}. Must be between {cls.__MIN_RGB_FLOAT_VAL} and {cls.__MAX_RGB_FLOAT_VAL}.")

        return value

    @classmethod
    def __rgb_uint8_to_float(cls, value: int) -> float:
        return float(value*(cls.__MAX_RGB_FLOAT_VAL-cls.__MIN_RGB_FLOAT_VAL)/(cls.__MAX_RGB_UINT8_VAL-cls.__MIN_RGB_UINT8_VAL))

    @classmethod
    def __rgb_float_to_uint8(cls, value: float) -> int:
        return int(round(value*(cls.__MAX_RGB_UINT8_VAL-cls.__MIN_RGB_UINT8_VAL)/(cls.__MAX_RGB_FLOAT_VAL-cls.__MIN_RGB_FLOAT_VAL)))
    
    def __get_r_8bit(self) -> int:
        return self.__rgb_float_to_uint8(self.__r)
    
    def __set_r_8bit(self, value: int):
        value = self.__check_rgb_uint8_value(value)
        self.__r = self.__rgb_uint8_to_float(value)

    def __get_g_8bit(self) -> int:
        return self.__rgb_float_to_uint8(self.__g)
    
    def __set_g_8bit(self, value: int):
        value = self.__check_rgb_uint8_value(value)
        self.__g = self.__rgb_uint8_to_float(value)

    def __get_b_8bit(self) -> int:
        return self.__rgb_float_to_uint8(self.__b)
    
    def __set_b_8bit(self, value: int):
        value = self.__check_rgb_uint8_value(value)
        self.__b = self.__rgb_uint8_to_float(value)

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
                raise ValueError(f"{self.__class__.__name__} {self.__name__} has invalid or not implemented value for color_mode ({self.color_mode}).")

    def __set_r(self, value: float | int):
        
        match self.color_mode:
            case COLOR_MODE.FLOAT_0_TO_1:
                self.r_float = value
            case COLOR_MODE.UINT8:
                self.r_8bit = value
            case _:
                raise ValueError(f"{self.__class__.__name__} {self.__name__} has invalid or not implemented value for color_mode ({self.color_mode}).")

    def __get_g(self) -> float:

        match self.color_mode:
            case COLOR_MODE.FLOAT_0_TO_1:
                return self.g_float
            case COLOR_MODE.UINT8:
                return self.g_8bit
            case _:
                raise ValueError(f"{self.__class__.__name__} {self.__name__} has invalid or not implemented value for color_mode ({self.color_mode}).")
    
    def __set_g(self, value: float | int):
        
        match self.color_mode:
            case COLOR_MODE.FLOAT_0_TO_1:
                self.g_float = value
            case COLOR_MODE.UINT8:
                self.g_8bit = value
            case _:
                raise ValueError(f"{self.__class__.__name__} {self.__name__} has invalid or not implemented value for color_mode ({self.color_mode}).")

    def __get_b(self) -> float:

        match self.color_mode:
            case COLOR_MODE.FLOAT_0_TO_1:
                return self.b_float
            case COLOR_MODE.UINT8:
                return self.b_8bit
            case _:
                raise ValueError(f"{self.__class__.__name__} {self.__name__} has invalid or not implemented value for color_mode ({self.color_mode}).")
    
    def __set_b(self, value: float | int):
        
        match self.color_mode:
            case COLOR_MODE.FLOAT_0_TO_1:
                self.b_float = value
            case COLOR_MODE.UINT8:
                self.b_8bit = value
            case _:
                raise ValueError(f"{self.__class__.__name__} {self.__name__} has invalid or not implemented value for color_mode ({self.color_mode}).")

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
        return f"Color(r={self.r}, g={self.g}, b={self.b})"