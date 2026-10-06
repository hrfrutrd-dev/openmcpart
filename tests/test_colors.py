from openmcpart.utils.color_utils import (
    hex_to_rgb,
    rgb_to_hex,
    contrast_ratio,
    wcag_level,
    generate_harmony,
    generate_palette_from_mood,
)
from openmcpart.tools.colors import (
    tool_generate_color_palette,
    tool_check_color_contrast,
    tool_generate_gradient,
)

def test_hex_to_rgb():
    assert hex_to_rgb("#ffffff") == (255, 255, 255)
    assert hex_to_rgb("#000000") == (0, 0, 0)
    assert hex_to_rgb("#3b82f6") == (59, 130, 246)
    assert hex_to_rgb("fff") == (255, 255, 255)

def test_contrast():
    ratio = contrast_ratio("#ffffff", "#000000")
    assert ratio == 21.0
    ratio2 = contrast_ratio("#ffffff", "#ffffff")
    assert ratio2 == 1.0

def test_wcag():
    levels = wcag_level(7.5)
    assert levels["AA_normal"] is True
    assert levels["AAA_normal"] is True
    levels2 = wcag_level(3.0)
    assert levels2["AA_normal"] is False
    assert levels2["AA_large"] is True

def test_harmony():
    comp = generate_harmony("#ff0000", "complementary")
    assert len(comp) == 2
    tri = generate_harmony("#ff0000", "triadic")
    assert len(tri) == 3

def test_mood_palette():
    palette = generate_palette_from_mood("calm")
    assert "primary" in palette
    assert "secondary" in palette

def test_generate_palette_tool():
    result = tool_generate_color_palette(base_color="#3b82f6", harmony="complementary")
    assert "harmony_colors" in result
    assert "css_variables" in result

def test_contrast_tool():
    result = tool_check_color_contrast("#ffffff", "#000000")
    assert result["ratio"] == 21.0
    assert result["wcag"]["AAA_normal"] is True

def test_gradient_tool():
    result = tool_generate_gradient("#ff0000", "#0000ff", "linear", 135)
    assert "css" in result
    assert "tailwind" in result
