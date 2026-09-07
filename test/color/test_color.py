from isa_utils import color

def test_color_instantiation():

    test_color = color.Color(color_mode = color.COLOR_MODES.FLOAT_0_TO_1)
    assert test_color.rgb == (0, 0, 0)

def test_color_instantiation_one_argument():

    for c in (0, 1, 0.5, 0.33, 0.9999999, 1e-70, 1 - 1e-70):
        test_color = color.Color(c, color_mode = color.COLOR_MODES.FLOAT_0_TO_1)
        assert test_color.rgb == (c, c, c)

def test_color_instantiation_three_arguments():
    """
    Tests to make sure that arguments don't get shuffled around.
    """

    r, g, b = (0.1, 0.2, 0.3)
    test_color = color.Color(r, g, b, color_mode = color.COLOR_MODES.FLOAT_0_TO_1)
    assert test_color.rgb == (r, g, b)

def test_color_instantiation_8_bit():
    
    test_color = color.Color(color_mode = color.COLOR_MODES.UINT8)
    assert test_color.rgb == (0, 0, 0)

def test_color_instantiation_one_argument_8_bit():

    for c in range(256):
        test_color = color.Color(c, color_mode = color.COLOR_MODES.UINT8)
        assert test_color.rgb == (c, c, c)


def test_conversion_from_float_to_8bit():

    test_color = color.Color(0.33, 0.75, 1, color_mode = color.COLOR_MODES.FLOAT_0_TO_1)
    assert test_color.rgb_24bit == (84, 191, 255)


def test_edge_case_conversion_from_float_to_8bit():

    test_color = color.Color(1e-20, 1 - 1e-20, 1, color_mode = color.COLOR_MODES.FLOAT_0_TO_1)
    assert test_color.rgb_24bit == (0, 254, 255)

def test_conversion_from_8bit_to_float():

    r_8bit, g_8bit, b_8bit = 60, 120, 180
    r_float, g_float, b_float = 0.2352941176, 0.4705882353, 0.7058823529

    test_color = color.Color(r_8bit, g_8bit, b_8bit, color_mode = color.COLOR_MODES.UINT8)
    assert test_color.rgb_float == (r_float, g_float, b_float)

    test_color.color_mode = color.COLOR_MODES.FLOAT_0_TO_1
    assert test_color.rgb == (r_float, g_float, b_float)

def test_illegal_values_for_color_instantiation():
    pass