"""
Submodule that implements a basic color class.
"""

# ---------------------------------------------------------------------------- #
#                                    Classes                                   #
# ---------------------------------------------------------------------------- #

class Color():

    def __init__(self, *args, **kwargs):

        match len(args):
            case 0:
                # Defaults
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

        

    # -------------------------- Properties: r, g and b -------------------------- #
    
    def __get_r(self):
        return self.__r

    def __set_r(self, value: float):
        self.__r = min(max(value, 0), 1)

    def __get_g(self):
            return self.__g
    
    def __set_g(self, value: float):
        self.__g = min(max(value, 0), 1)

    def __get_b(self):
            return self.__b
    
    def __set_b(self, value: float):
        self.__b = min(max(value, 0), 1)

    r = property(__get_r, __set_r)
    g = property(__get_g, __set_g)
    b = property(__get_b, __set_b)