from openmcpart.tools.accessibility import tool_check_accessibility
from openmcpart.tools.colors import tool_generate_color_palette
from openmcpart.tools.tokens import tool_generate_design_tokens, tool_generate_tailwind_config
from openmcpart.tools.colors import tool_check_color_contrast, tool_generate_gradient
from openmcpart.tools.ui_generator import tool_critique_ai_look, tool_generate_sophisticated_ui
from openmcpart.tools.accessibility import tool_critique_design, tool_suggest_component_variants
from openmcpart.tools.branding import tool_generate_moodboard_brief
from openmcpart.tools.layout import tool_generate_spacing_system, tool_suggest_layout
from openmcpart.tools.typography import tool_generate_type_scale, tool_suggest_typography_pairing
from openmcpart.utils.color_utils import hex_to_rgb


def test_palette_respects_requested_count_for_base_and_mood():
    assert tool_generate_color_palette(base_color="#3b82f6", count=7)["count"] == 7
    assert tool_generate_color_palette(mood="calm", count=3)["count"] == 3


def test_palette_honors_harmony_for_moods_and_defaults_to_tech():
    triadic = tool_generate_color_palette(mood="calm", harmony="triadic", count=5)
    default = tool_generate_color_palette()

    calm = tool_generate_color_palette(mood="calm")
    assert triadic["harmony_type"] == "triadic"
    assert len(triadic["harmony_colors"]) == 3
    assert calm["secondary"] != calm["accent"]
    assert triadic["count"] == 5
    assert triadic["full_palette"][0] == triadic["usage"]["primary"]
    assert default["mood"] == "tech"
    assert default["default_mood_used"] is True


def test_palette_rejects_unsupported_values():
    analogous = tool_generate_color_palette(base_color="#3b82f6", harmony="analogous")
    assert analogous["usage"]["secondary"] != analogous["usage"]["primary"]
    assert analogous["full_palette"][0] == analogous["usage"]["primary"]
    assert "error" in tool_generate_color_palette(base_color="#123456", harmony="unknown")
    assert "error" in tool_generate_color_palette(base_color="#123456", count=11)


def test_hex_parser_rejects_multiple_prefixes_and_non_hex():
    for value in ("##fff", "#ggg", "12345", "#12345678"):
        try:
            hex_to_rgb(value)
        except ValueError:
            continue
        raise AssertionError(f"Expected {value!r} to be rejected")


def test_contrast_suggestions_only_include_passing_pairs():
    result = tool_check_color_contrast("#fff", "#777777")

    assert result["foreground"] == "#ffffff"
    assert result["background"] == "#777777"
    assert result["suggestions"]["accessible_pairs"]
    assert all(pair["ratio"] >= 4.5 for pair in result["suggestions"]["accessible_pairs"])
    assert all(pair["wcag_aa_normal_text"] for pair in result["suggestions"]["accessible_pairs"])


def test_gradient_resolves_hex_values_and_matches_requested_style():
    radial = tool_generate_gradient("fff", "000", style="radial")
    conic = tool_generate_gradient("#123", "#abc", style="conic", angle=45)

    assert radial["from"] == "#ffffff"
    assert radial["css"]["with_mid"].startswith("radial-gradient(")
    assert conic["css"]["with_mid"].startswith("conic-gradient(from 45deg,")
    assert "error" in tool_generate_gradient("#fff", "#000", style="unknown")
    assert "error" in tool_generate_gradient("#fff", "#000", angle=999)


def test_layout_and_component_tools_reject_unsupported_values():
    assert "error" in tool_suggest_layout("dashboard", target="phone")
    assert "error" in tool_suggest_layout("dashboard", style="universal")
    assert "error" in tool_generate_spacing_system(base=1)
    assert "error" in tool_generate_spacing_system(max_scale=100)
    assert "error" in tool_suggest_component_variants("button", count=0)
    assert "error" in tool_suggest_component_variants("button", style="unknown")


def test_typography_tools_validate_scale_inputs_and_language_tags():
    assert tool_generate_type_scale(ratio="not-a-ratio")["error"].startswith("Unsupported ratio")
    assert "error" in tool_generate_type_scale(base_size=9)
    assert tool_suggest_typography_pairing(language="ja-JP")["matched_style"] == "japanese_modern"
    assert tool_suggest_typography_pairing(language="javascript")["matched_style"] == "modern_minimal"
    assert tool_suggest_typography_pairing(industry="fashion")["matched_style"] == "elegant_luxury"


def test_design_tokens_use_resolved_colors_and_portable_outputs():
    result = tool_generate_design_tokens(primary_color="#3b82f6", radius="none")

    assert "error" not in result
    assert result["tokens"]["color"]["primary"]["500"] == "#3b82f6"
    assert result["tokens"]["color"]["primary"]["100"].startswith("#")
    assert "color-mix(" not in result["json"]
    assert "--color-primary-500: #3b82f6;" in result["css_variables"]
    assert '"$type": "color"' in result["dtcg_json"]
    assert '"md": "0px"' in result["json"]


def test_design_token_generation_validates_inputs_and_escapes_css():
    invalid = tool_generate_design_tokens(primary_color="red")
    css = tool_generate_design_tokens(font_heading="O'Reilly */\nInjected")

    assert "error" in invalid
    assert "--font-heading: 'O\\'Reilly */ Injected', sans-serif;" in css["css_variables"]
    assert tool_generate_design_tokens(radius="unknown")["error"].startswith("Unsupported radius")
    assert "error" in tool_generate_tailwind_config(primary="not-a-color")


def test_accessibility_size_supports_decimal_rem_and_does_not_claim_a_score():
    result = tool_check_accessibility(font_size="1.25rem")
    size_check = next(check for check in result["specific_checks"] if check["item"] == "テキストサイズ")

    assert size_check["estimated_px"] == 20
    assert "score" not in result["summary"]
    assert "適合証明" in result["summary"]["note"]


def test_moodboard_generation_does_not_mutate_shared_presets():
    first = tool_generate_moodboard_brief("minimal", "calm")
    first["colors"].append("#123456")
    second = tool_generate_moodboard_brief("minimal", "bright")

    assert "#123456" not in second["colors"]
    assert second["requested_theme"] == "minimal"
    assert second["keywords"] == "bright"


def test_ui_generator_respects_selected_aesthetic_and_avoidance_toggle():
    profile = tool_generate_sophisticated_ui(aesthetic="clay_moss", avoid_ai_tropes=False)
    editorial = tool_generate_sophisticated_ui(aesthetic="editorial", avoid_ai_tropes=False)

    assert profile["palette"]["name"] == "Clay & Moss"
    assert profile["ai_tropes_to_avoid"] == []
    assert "* { border-radius: 0; }" not in profile["css_variables"]
    assert "boxShadow: { sm:" in profile["tailwind_config"]
    assert "Suisse Int\\'l" in editorial["css_variables"]
    assert "error" in tool_generate_sophisticated_ui(aesthetic="unknown")


def test_design_critique_uses_neutral_review_prompts_for_neutral_descriptions():
    result = tool_critique_design("A blue SaaS page with a button and a clear product description")

    assert result["analysis_type"] == "keyword_heuristic"
    assert result["critique"] == []
    assert "scores" not in result
    assert result["limitations"]


def test_design_critique_flags_only_explicit_concerns_and_filters_focus():
    result = tool_critique_design("CTAが目立たない。テキストは低コントラスト", focus="contrast")

    assert result["focus"] == "contrast"
    assert len(result["heuristics"]) == 1
    assert len(result["critique"]) == 2
    assert all(item["status"] == "review_requested_by_description" for item in result["critique"])
    assert "error" in tool_critique_design("neutral page", focus="unknown")


def test_aesthetic_critique_only_flags_described_patterns():
    result = tool_critique_ai_look("写真中心の落ち着いたECサイト")

    assert result["detected_ai_tropes"] == []
    assert result["suggestions"] == []
    assert "普遍的な品質問題" in result["aesthetic_note"]


def test_aesthetic_critique_detects_japanese_pattern():
    result = tool_critique_ai_look("紫グラデと24pxの丸いカード")

    assert len(result["detected_ai_tropes"]) == 2
    assert all(item["priority"] == "optional_style_change" for item in result["suggestions"])
