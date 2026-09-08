import pytest

from isa_utils import color

class Test_Color_Instantiation():

    def test_no_args(self):
        test_color = color.Color()
        assert test_color.color_mode == color.COLOR_MODE.FLOAT_0_TO_1
        assert test_color.rgb == (0, 0, 0)

    @pytest.mark.parametrize(
        ("color_mode", "c"),
        [(color.COLOR_MODE.FLOAT_0_TO_1, value) for value in (0, 0.5, 1)] +
        [(color.COLOR_MODE.UINT8, value) for value in (0, 127, 255)]
    )
    def test_one_channel_arg(self, color_mode, c):
        test_color = color.Color(c, color_mode=color_mode)
        assert test_color.rgb == (c, c, c)

    @pytest.mark.parametrize(
        ("color_mode", "r", "g", "b"), [
            (color.COLOR_MODE.FLOAT_0_TO_1, 0.2, 0.5, 0.8),
            (color.COLOR_MODE.UINT8, 30, 120, 210)
        ]
    )
    def test_three_args(self, color_mode, r, g, b):
        test_color = color.Color(r, g, b, color_mode = color_mode)
        assert test_color.rgb == (r, g, b)

    @pytest.mark.parametrize(
        ("color_mode", "c", "expected_exception_type"),
        [(color.COLOR_MODE.FLOAT_0_TO_1, value, exception_type) for value, exception_type in (("banana", TypeError), (-0.1, ValueError), (255, ValueError))] +
        [(color.COLOR_MODE.UINT8, value, exception_type) for value, exception_type in (("banana", TypeError), (-1, ValueError), (256, ValueError))]
    )
    def test_illegal_args(self, color_mode, c, expected_exception_type):

        with pytest.raises(expected_exception_type):
            test_color = color.Color(c, color_mode=color_mode)

class Test_Value_Conversion():

    def test_conversion_from_float_to_8bit(self):

        test_color = color.Color(0.33, 0.75, 1, color_mode = color.COLOR_MODE.FLOAT_0_TO_1)
        assert test_color.rgb_24bit == (84, 191, 255)


    def test_edge_case_conversion_from_float_to_8bit(self):

        test_color = color.Color(1e-20, 1 - 1e-20, 1, color_mode = color.COLOR_MODE.FLOAT_0_TO_1)
        assert test_color.rgb_24bit == (0, 254, 255)

    def test_conversion_from_8bit_to_float(self):

        r_8bit, g_8bit, b_8bit = 60, 120, 180
        r_float, g_float, b_float = 0.2352941176, 0.4705882353, 0.7058823529

        test_color = color.Color(r_8bit, g_8bit, b_8bit, color_mode = color.COLOR_MODE.UINT8)
        assert test_color.rgb_float == pytest.approx((r_float, g_float, b_float))

        test_color.color_mode = color.COLOR_MODE.FLOAT_0_TO_1
        assert test_color.rgb == pytest.approx((r_float, g_float, b_float))

def test_values_for_color_mode():
    
    test_color = color.Color(color_mode = 1)
    test_color = color.Color(color_mode = 1.0)

    with pytest.raises(ValueError):
        test_color = color.Color(color_mode = 1.5)
    with pytest.raises(ValueError):
        test_color = color.Color(color_mode = color.COLOR_MODE._add_alias_)
    with pytest.raises(ValueError):
        test_color = color.Color(color_mode = "UINT8")