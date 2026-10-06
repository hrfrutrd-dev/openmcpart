# 使用例集

## 1. カラーパレット生成

### プロンプト
```
SaaSのランディングページ用に、#3b82f6をベースにしたカラーパレットを作って
```

### Agentの動き
```python
generate_color_palette(base_color="#3b82f6", harmony="analogous")
```

### 出力活用
```css
:root {
  --color-primary: #3b82f6;
  --color-secondary: #6b7ef0;
  --color-accent: #f59e0b;
}
```

---

## 2. コントラストチェック

### プロンプト
```
このボタンのコントラストは大丈夫？ 白文字 #ffffff に青背景 #3b82f6
```

### Agentの動き
```python
check_color_contrast(foreground="#ffffff", background="#3b82f6")
```

### 出力
- Ratio: 4.52
- AA_normal: Pass
- AAA_normal: Fail
- 色覚多様性シミュレーションも含む

---

## 3. タイポグラフィ

### プロンプト
```
日本語のテック系メディア向けフォントペアリングを教えて
```

### Agentの動き
```python
suggest_typography_pairing(mood="tech_trust", industry="media", language="ja")
```

### 出力
- Heading: Noto Sans JP
- Body: Noto Sans JP
- Type scale: xs〜5xl
- CSS import文付き

---

## 4. レイアウト提案

### プロンプト
```
ダッシュボードのレイアウトを考えて。モダンでミニマルに
```

### Agentの動き
```python
suggest_layout(content_type="dashboard", target="desktop", style="minimal")
```

### 出力
- セクション構成
- グリッド: 12col
- スペーシング: 8pt grid
- 実装コード (CSS & Tailwind)

---

## 5. デザインシステム構築

### プロンプト
```
ブランド名 TechFlow、プライマリ #6366f1 でデザインシステム作って
```

### Agentの動き
```python
generate_design_tokens(primary_color="#6366f1", brand_name="TechFlow", radius="medium")
generate_tailwind_config(primary="#6366f1", style="modern")
```

### 出力
- 完全なトークンJSON
- CSS変数
- Tailwind config
- Figma Tokens対応

---

## 6. アクセシビリティ監査

### プロンプト
```
このフォームのアクセシビリティをチェックして
```

### Agentの動き
```python
check_accessibility(description="ログインフォーム、メールとパスワード", interactive=True, font_size="16px")
```

### 出力
- チェックリスト (Perceivable, Operable, Understandable, Robust)
- クイックウィン5つ
- 推奨ツール

---

## 7. デザイン批評

### プロンプト
```
このランディングページを批評して: ヒーローが弱い、CTAが目立たない、情報が多い
```

### Agentの動き
```python
critique_design(design_description="SaaSランディング、ヒーローが弱い、CTAが目立たない、情報が多い", focus="all")
```

### 出力
- 8原則での評価
- 具体的な問題と重症度
- Immediate / Short-term / Long-term アクションプラン

---

## 8. ブランディング

### プロンプト
```
ブランドキーワード: 信頼,革新,親しみ からデザイン方向性を出して
```

### Agentの動き
```python
extract_design_principles(brand_keywords="信頼,革新,親しみ", industry="SaaS", audience="スタートアップ")
```

### 出力
- ブランドアーキタイプ (例: Sage, Creator)
- カラー心理学
- タイポグラフィ方向性
- ネクストステップ

---

## 9. ムードボード

### プロンプト
```
ミニマルで日本的なムードボードを作って
```

### Agentの動き
```python
generate_moodboard_brief(theme="japanese", keywords="minimal, zen")
```

### 出力
- カラー
- フォント
- イメージ方向性
- テクスチャ
- 参考ブランド
- ブリーフテンプレート

---

## 10. コンポーネント設計

### プロンプト
```
モダンなボタンのバリエーションをTailwindで5種類
```

### Agentの動き
```python
suggest_component_variants(component="button", style="modern", count=5)
```

### 出力
- Primary, Secondary, Ghost, Destructive, Link
- サイズ: sm, md, lg
- 状態: hover, focus, disabled...
- a11y考慮
- コード例 (HTML, React)

---

## ワークフロー例: ゼロからSaaSランディングを作る

1. **ブランディング**
   ```
   extract_design_principles("信頼,革新,シンプル", "SaaS")
   → アーキタイプ: Sage, カラー: 青系
   ```

2. **カラー**
   ```
   generate_color_palette(mood="tech", harmony="analogous")
   → primary, secondary, accent決定
   ```

3. **タイポ**
   ```
   suggest_typography_pairing(mood="tech_trust", industry="saas")
   → Inter + Inter
   ```

4. **トークン**
   ```
   generate_design_tokens(primary="#3b82f6", brand_name="MySaaS")
   → 完全なデザインシステム
   ```

5. **レイアウト**
   ```
   suggest_layout("landing_saas", "desktop", "minimal")
   → セクション構成、グリッド
   ```

6. **コンポーネント**
   ```
   suggest_component_variants("button", "modern", 3)
   → CTAボタン設計
   ```

7. **チェック**
   ```
   check_color_contrast("#ffffff", "#3b82f6")
   check_accessibility("SaaSランディングヒーロー", "#ffffff", "#3b82f6")
   critique_design("SaaSランディング、作成したデザイン...")
   ```

これで、どんなAgentでもプロレベルのデザインを作成可能！
