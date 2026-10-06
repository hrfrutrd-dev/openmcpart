"""
Branding and design principles tools
"""
from typing import Dict, Any, List

BRAND_ARCHETYPES = {
    "innocent": {"keywords": ["純粋", "正直", "楽観", "シンプル"], "colors": ["#fef3c7", "#fde68a", "#ffffff"], "fonts": "丸みのあるサンセリフ", "imagery": "明るく、清潔、自然光"},
    "explorer": {"keywords": ["自由", "冒険", "独立", "発見"], "colors": ["#065f46", "#d97706", "#1f2937"], "fonts": "力強いサンセリフ", "imagery": "広大な自然、冒険、道"},
    "sage": {"keywords": ["知恵", "知識", "真実", "洞察"], "colors": ["#1e3a8a", "#f3f4f6", "#6b7280"], "fonts": "セリフ、知的", "imagery": "本、学び、落ち着いた"},
    "hero": {"keywords": ["勇気", "力", "達成", "大胆"], "colors": ["#991b1b", "#111827", "#fbbf24"], "fonts": "太い、力強い", "imagery": "動き、達成、強いコントラスト"},
    "outlaw": {"keywords": ["反抗", "自由", "破壊", "革新"], "colors": ["#000000", "#ef4444", "#ffffff"], "fonts": "荒々しい、グランジ", "imagery": "破壊、反抗、ダーク"},
    "magician": {"keywords": ["変容", "夢", "神秘", "ビジョン"], "colors": ["#5b21b6", "#0f172a", "#e879f9"], "fonts": "エレガント、神秘的", "imagery": "変容、光、夢"},
    "regular": {"keywords": ["親しみ", "所属", "平等", "現実"], "colors": ["#3b82f6", "#f3f4f6", "#1f2937"], "fonts": "親しみやすいサンセリフ", "imagery": "日常、人々、共感"},
    "lover": {"keywords": ["愛", "親密", "情熱", "美"], "colors": ["#be185d", "#fce7f3", "#111827"], "fonts": "エレガント、柔らかい", "imagery": "美、親密、官能的"},
    "jester": {"keywords": ["楽しさ", "ユーモア", "遊び心", "楽観"], "colors": ["#f59e0b", "#ec4899", "#3b82f6"], "fonts": "楽しい、手書き風", "imagery": "遊び、笑い、カラフル"},
    "caregiver": {"keywords": ["思いやり", "ケア", "育む", "安心"], "colors": ["#059669", "#d1fae5", "#ffffff"], "fonts": "柔らかい、温かみ", "imagery": "ケア、手、温かみ"},
    "creator": {"keywords": ["創造", "想像", "表現", "芸術"], "colors": ["#7c3aed", "#f5f3ff", "#111827"], "fonts": "創造的、個性的", "imagery": "制作過程、アート、色"},
    "ruler": {"keywords": ["統制", "権威", "高級", "責任"], "colors": ["#111827", "#d4af37", "#f3f4f6"], "fonts": "クラシック、権威", "imagery": "高級、権威、整然"},
}

def tool_extract_design_principles(brand_keywords: str, industry: str = "", audience: str = "") -> Dict[str, Any]:
    keywords = [k.strip().lower() for k in brand_keywords.replace("、", ",").split(",")]
    
    # Match archetype
    best_match = None
    max_score = 0
    for archetype, data in BRAND_ARCHETYPES.items():
        score = 0
        for kw in keywords:
            for brand_kw in data["keywords"]:
                if kw in brand_kw or brand_kw in kw:
                    score += 2
            if kw in archetype:
                score += 1
        if score > max_score:
            max_score = score
            best_match = archetype
    
    if not best_match:
        best_match = "regular"
    
    archetype_data = BRAND_ARCHETYPES[best_match]
    
    # Generate principles
    principles = []
    if "シンプル" in brand_keywords or "minimal" in brand_keywords.lower():
        principles.append({"principle": "Less is More", "description": "要素を削ぎ落とし、本質だけを残す", "application": "余白を大胆に、色は3色まで、フォントは2種類まで"})
    if "信頼" in brand_keywords or "trust" in brand_keywords.lower():
        principles.append({"principle": "信頼性", "description": "一貫性と安定感で信頼を構築", "application": "グリッド準拠、予測可能なインタラクション、実績の提示"})
    if "革新" in brand_keywords or "innovative" in brand_keywords.lower():
        principles.append({"principle": "革新性", "description": "既存の枠を超える", "application": "非対称レイアウト、大胆なタイポ、実験的なインタラクション"})
    
    # Default principles if none matched
    if not principles:
        principles = [
            {"principle": "明快性 (Clarity)", "description": "迷わせない、瞬時に理解できる", "application": "明確な階層、直感的なラベル、視覚的手がかり"},
            {"principle": "一貫性 (Consistency)", "description": "予測可能で学習しやすい", "application": "デザインシステム、パターンの再利用"},
            {"principle": "人間中心 (Human-centered)", "description": "人のニーズを最優先", "application": "ユーザーリサーチ、アクセシビリティ、エンパシー"},
        ]
    
    # Color psychology
    color_psych = {
        "red": "情熱、エネルギー、緊急性",
        "blue": "信頼、冷静、プロフェッショナル",
        "green": "成長、自然、安心",
        "yellow": "楽観、注意、親しみ",
        "purple": "創造性、高級、神秘",
        "orange": "親しみ、活力、自信",
        "black": "高級、力、洗練",
        "white": "清潔、シンプル、広がり",
    }
    
    # Industry specific
    industry_tips = ""
    if industry:
        industry_lower = industry.lower()
        if "tech" in industry_lower or "saas" in industry_lower:
            industry_tips = "SaaS: 信頼感(青) + 余白多め + データ可視化を明確に"
        elif "fashion" in industry_lower:
            industry_tips = "ファッション: 大胆なタイポ、大きなビジュアル、余白で高級感"
        elif "finance" in industry_lower:
            industry_tips = "金融: 信頼(濃い青)、セキュリティ感、数字の可読性"
        elif "health" in industry_lower:
            industry_tips = "ヘルスケア: 安心感(緑/青)、柔らかさ、アクセシビリティ最優先"
    
    return {
        "input": {"keywords": brand_keywords, "industry": industry, "audience": audience},
        "matched_archetype": {"name": best_match, **archetype_data},
        "all_archetypes": list(BRAND_ARCHETYPES.keys()),
        "design_principles": principles,
        "color_psychology": color_psych,
        "suggested_palette": archetype_data["colors"],
        "typography_direction": archetype_data["fonts"],
        "imagery_direction": archetype_data["imagery"],
        "voice_and_tone": {
            "innocent": "正直、謙虚、楽観的",
            "explorer": "大胆、自由、冒険的",
            "sage": "知的、信頼できる、思慮深い",
        }.get(best_match, "親しみやすく、明確に、自信を持って"),
        "industry_tip": industry_tips,
        "next_steps": [
            "1. ムードボード作成: 競合3社 + 理想のブランド3社のスクショを集める",
            "2. 3色パレット決定: 60-30-10ルールで",
            "3. タイポグラフィ決定: 見出し1 + 本文1",
            "4. ロゴとキービジュアルの方向性決定",
            "5. コンポーネントの雰囲気決め (角丸、影、密度)"
        ]
    }

def tool_generate_moodboard_brief(theme: str, keywords: str = "") -> Dict[str, Any]:
    theme = theme.lower()
    
    moods = {
        "minimal": {
            "colors": ["#ffffff", "#f5f5f5", "#111111", "#e5e7eb"],
            "fonts": "Inter, Helvetica Neue",
            "imagery": "余白、モノクロ、プロダクトのみ、影は柔らかく",
            "textures": "紙、マット、コンクリート",
            "references": "Apple, Muji, Linear",
        },
        "brutalism": {
            "colors": ["#000000", "#ffffff", "#ff0000", "#ffff00"],
            "fonts": "Monospace, 太いサンセリフ",
            "imagery": "生のHTML感、太いボーダー、非対称",
            "textures": "荒い、コンクリート、ノイズ",
            "references": "Gumroad, Brutalist Websites",
        },
        "glassmorphism": {
            "colors": ["#e0e7ff", "#c7d2fe", "#a5b4fc", "rgba(255,255,255,0.2)"],
            "fonts": "SF Pro, Inter, 柔らかい",
            "imagery": "すりガラス、ぼかし、奥行き、光",
            "textures": "ガラス、ぼかし、グラデーション",
            "references": "Apple Vision Pro, Stripe",
        },
        "neomorphism": {
            "colors": ["#e0e5ec", "#d1d9e6", "#a3b1c6"],
            "fonts": "柔らかいサンセリフ",
            "imagery": "柔らかい押し出し、影で立体感",
            "textures": "粘土、柔らかいプラスチック",
            "references": "初期のNeumorphismトレンド",
        },
        "japanese": {
            "colors": ["#f5f1e8", "#2c2c2c", "#c41e3a", "#2a6b4f"],
            "fonts": "Noto Serif JP, Zen Kaku Gothic",
            "imagery": "余白、非対称、自然素材、引き算",
            "textures": "和紙、木、石",
            "references": "無印良品、隈研吾、原研哉",
        },
        "y2k": {
            "colors": ["#ff00ff", "#00ffff", "#ffff00", "#000000"],
            "fonts": "バブル、ピクセル、太い",
            "imagery": "メタリック、虹色、ローテク、ノスタルジア",
            "textures": "メタリック、プラスチック、グリッチ",
            "references": "2000年代ウェブ、PC Music",
        }
    }
    
    matched = None
    for key in moods:
        if key in theme or theme in key:
            matched = key
            break
    if not matched:
        matched = "minimal"
    
    data = moods[matched]
    data["theme"] = matched
    data["requested_theme"] = theme
    data["keywords"] = keywords
    
    data["brief_template"] = f"""
# Moodboard Brief: {matched.title()}

## Theme
{theme} - {keywords}

## Colors
{', '.join(data['colors'])}

## Typography
{data['fonts']}

## Imagery Direction
{data['imagery']}

## Textures / Materials
{data['textures']}

## Reference Brands
{data['references']}

## Do's and Don'ts
- Do: 一貫性を保つ、余白を恐れない
- Don't: トレンドをそのままコピー、要素を詰め込みすぎない

## Deliverables
- [ ] 10枚の参考画像収集
- [ ] 3色パレット確定
- [ ] フォント2種確定
- [ ] キービジュアル1枚作成
"""
    
    return data
