// openmcpart Playground - Sophisticated, Non-AI JS
// Implements MCP tools in browser with same logic

// Color utils (same as Python)
function hexToRgb(hex) {
  hex = hex.replace('#', '');
  if (hex.length === 3) hex = hex.split('').map(c => c+c).join('');
  return {
    r: parseInt(hex.slice(0,2), 16),
    g: parseInt(hex.slice(2,4), 16),
    b: parseInt(hex.slice(4,6), 16)
  };
}

function rgbToHsl(r, g, b) {
  r/=255; g/=255; b/=255;
  const max = Math.max(r,g,b), min = Math.min(r,g,b);
  let h, s, l = (max+min)/2;
  if (max===min) { h=s=0; }
  else {
    const d = max-min;
    s = l>0.5 ? d/(2-max-min) : d/(max+min);
    switch(max) {
      case r: h = (g-b)/d + (g<b?6:0); break;
      case g: h = (b-r)/d + 2; break;
      case b: h = (r-g)/d + 4; break;
    }
    h/=6;
  }
  return { h: h*360, s: s*100, l: l*100 };
}

function hslToHex(h, s, l) {
  h = (h%360)/360; s=Math.max(0,Math.min(100,s))/100; l=Math.max(0,Math.min(100,l))/100;
  let r,g,b;
  if (s===0) r=g=b=l;
  else {
    const hue2rgb = (p,q,t) => {
      if(t<0) t+=1; if(t>1) t-=1;
      if(t<1/6) return p + (q-p)*6*t;
      if(t<1/2) return q;
      if(t<2/3) return p + (q-p)*(2/3-t)*6;
      return p;
    };
    const q = l<0.5 ? l*(1+s) : l+s-l*s;
    const p = 2*l-q;
    r = hue2rgb(p,q,h+1/3);
    g = hue2rgb(p,q,h);
    b = hue2rgb(p,q,h-1/3);
  }
  return `#${Math.round(r*255).toString(16).padStart(2,'0')}${Math.round(g*255).toString(16).padStart(2,'0')}${Math.round(b*255).toString(16).padStart(2,'0')}`;
}

function contrastRatio(fg, bg) {
  const luminance = (hex) => {
    const {r,g,b} = hexToRgb(hex);
    const linearize = (c) => {
      c/=255;
      return c<=0.04045 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4);
    };
    return 0.2126*linearize(r) + 0.7152*linearize(g) + 0.0722*linearize(b);
  };
  const l1 = luminance(fg), l2 = luminance(bg);
  const lighter = Math.max(l1,l2), darker = Math.min(l1,l2);
  return (lighter+0.05)/(darker+0.05);
}

// Sophisticated palettes - No AI purple
const SOPHISTICATED_PALETTES = {
  paper_ink: {
    name: "Paper & Ink",
    colors: { paper: "#fdfcfa", paper_dark: "#f5f3ef", ink: "#121212", hairline: "#e8e3dc", accent: "#c45a3c" },
    desc: "紙とインク - 最も洗練された基本"
  },
  clay_moss: {
    name: "Clay & Moss",
    colors: { paper: "#faf8f5", clay: "#c4a484", moss: "#5a6b5d", ink: "#1a1a18", stone: "#e8e0d5" },
    desc: "土と苔 - 日本的、工芸的"
  },
  editorial: {
    name: "Editorial Noir",
    colors: { paper: "#ffffff", ink: "#0a0a0a", gray_100: "#f5f5f3", gray_300: "#d4d4d0", accent: "#ff3b30" },
    desc: "モノクロ基調に1色だけ vivid"
  }
};

// Tool implementations
const tools = {
  sophisticated: {
    name: "generate_sophisticated_ui",
    controls: `
      <div class="control-group">
        <label>Purpose</label>
        <select id="purpose" class="input" style="border: 0.5px solid var(--hairline); padding: 0 12px;">
          <option value="landing page">landing page</option>
          <option value="dashboard">dashboard</option>
          <option value="portfolio">portfolio</option>
          <option value="editorial">editorial</option>
        </select>
      </div>
      <div class="control-group">
        <label>Aesthetic</label>
        <select id="aesthetic" class="input" style="border: 0.5px solid var(--hairline); padding: 0 12px;">
          <option value="paper_ink">paper_ink — Paper & Ink</option>
          <option value="clay_moss">clay_moss — Clay & Moss</option>
          <option value="editorial">editorial — Editorial Noir</option>
          <option value="atelier">atelier — Atelier</option>
        </select>
      </div>
      <button class="btn btn-primary" onclick="runTool('sophisticated')">Generate —</button>
    `,
    run: () => {
      const purpose = document.getElementById('purpose')?.value || 'landing page';
      const aesthetic = document.getElementById('aesthetic')?.value || 'paper_ink';
      const palette = SOPHISTICATED_PALETTES[aesthetic] || SOPHISTICATED_PALETTES.paper_ink;
      
      return {
        purpose,
        aesthetic,
        palette,
        typography: {
          heading: "Instrument Serif / Newsreader",
          body: "Inter Tight / Suisse Int'l",
          mono: "Fragment Mono",
          scale: "Heading 64px serif, line-height 0.95, tracking -0.02em. Body 15px, 1.7."
        },
        layout: {
          grid: "12col but asymmetrical: left 5col content, right 7col whitespace",
          whitespace: "Section 160-240px, not 80px. Fearless whitespace is sophistication.",
          borders: "0.5px hairline, no shadows",
          radius: "0px, max 4px if needed. Never 24px."
        },
        components: {
          button: "bg-ink text-paper, 0 radius, 44px height, 13px uppercase, 0.04em tracking, hover: opacity 0.85, no scale",
          card: "bg-paper, 0.5px border, 0 radius, 32px padding, no shadow, hover: border-color ink"
        },
        css_variables: `:root {
  --paper: ${palette.colors.paper};
  --ink: ${palette.colors.ink || '#121212'};
  --hairline: ${palette.colors.hairline || '#e8e3dc'};
  --accent: ${palette.colors.accent || '#c45a3c'};
  --font-serif: 'Instrument Serif', Georgia, serif;
  --font-sans: 'Inter Tight', system-ui, sans-serif;
  --radius: 0px;
  --hairline-border: 0.5px solid var(--hairline);
}
* { border-radius: 0 !important; }
body { background: var(--paper); color: var(--ink); }
h1 { font-family: var(--font-serif); font-size: 64px; line-height: 0.9; letter-spacing: -0.03em; }
.card { border: var(--hairline-border); background: var(--paper); padding: 32px; }
.btn { background: var(--ink); color: var(--paper); height: 44px; padding: 0 24px; border: 0; border-radius: 0; font-size: 13px; letter-spacing: 0.04em; text-transform: uppercase; }
.btn:hover { opacity: 0.85; } /* No scale */`,
        checklist: [
          "影を使っていないか？ → hairlineに",
          "角丸が24pxになっていないか？ → 0-4pxに",
          "紫→青グラデを使っていないか？ → 単色に",
          "中央揃えばかりでないか？ → 左揃え基本に",
          "余白が80pxで詰めていないか？ → 160pxに"
        ],
        avoids: ["Purple → Blue gradient", "Rounded 24px", "Shadow-lg", "✨ Magic", "Centered blob hero", "3-col icon grid"]
      };
    }
  },
  
  critique_ai: {
    name: "critique_ai_look",
    controls: `
      <div class="control-group">
        <label>Describe your design (AIっぽいデザインを説明)</label>
        <textarea id="designDesc" class="input" style="height: 80px; padding: 12px; border: 0.5px solid var(--hairline); resize: none;" placeholder="例: 紫グラデ背景に丸いカードが3列並ぶ、影が大きく、中央揃え、✨アイコン">紫グラデ背景に丸いカードが3列並ぶ、影が大きく、中央揃え、✨アイコン</textarea>
      </div>
      <button class="btn btn-primary" onclick="runTool('critique_ai')">Critique —</button>
    `,
    run: () => {
      const desc = document.getElementById('designDesc')?.value || '紫グラデ、丸いカード、影';
      const tropes = [
        { trope: "Purple → Blue gradient", why: "2023-24年のAIジェネリック", fix: "単色 + 紙の質感" },
        { trope: "Rounded 24px cards", why: "AIが好む安全な丸み", fix: "0-4px、sharpが洗練" },
        { trope: "Soft large shadows", why: "浮かせれば良いと思うAI", fix: "影なし + 0.5px hairline" },
        { trope: "Centered + blob", why: "全てのAI LPが同じ", fix: "左寄せ、右に大きく余白" },
      ];
      
      return {
        input: desc,
        detected: tropes,
        before: "紫グラデ + 24px角丸カード + shadow-lg + 中央揃え + ✨ + 3列アイコン",
        after: "紙色 #fdfcfa + 0px角 + 0.5px hairline + セリフ見出し + 左揃え + 160px余白",
        quick_fixes: [
          "背景を #fdfcfa (紙色) に",
          "角丸を 0px に",
          "影を消して 0.5px border に",
          "見出しを Instrument Serif に",
          "セクション間を 160px に",
          "中央揃えを左揃えに",
          "3列を1列 + 詳細に"
        ],
        css_fix: `/* Before - AIっぽい */
.ai-card {
  background: linear-gradient(135deg, #8b5cf6, #3b82f6);
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.12);
  text-align: center;
}

/* After - 洗練 */
.refined-card {
  background: #fdfcfa;
  border: 0.5px solid #e8e3dc;
  border-radius: 0;
  padding: 32px;
  text-align: left;
}
.refined-card:hover { border-color: #121212; }`
      };
    }
  },

  palette: {
    name: "generate_color_palette",
    controls: `
      <div class="control-group">
        <label>Base Color (hex)</label>
        <input id="baseColor" class="input" value="#121212" placeholder="#3b82f6">
      </div>
      <div class="control-group">
        <label>Mood (or leave empty if base color set)</label>
        <select id="mood" class="input" style="border: 0.5px solid var(--hairline); padding: 0 12px;">
          <option value="">—</option>
          <option value="paper_ink">paper_ink — No AI purple</option>
          <option value="calm">calm — 穏やか</option>
          <option value="tech">tech — 信頼</option>
          <option value="minimal">minimal — ミニマル</option>
        </select>
      </div>
      <button class="btn btn-primary" onclick="runTool('palette')">Generate Palette —</button>
    `,
    run: () => {
      const base = document.getElementById('baseColor')?.value || '#121212';
      const mood = document.getElementById('mood')?.value;
      
      if (mood === 'paper_ink' || !base) {
        return {
          mood: "paper_ink - AIっぽくない",
          primary: "#121212",
          secondary: "#fdfcfa",
          accent: "#c45a3c",
          neutrals: { paper: "#fdfcfa", paper_dark: "#f5f3ef", hairline: "#e8e3dc", ink: "#121212" },
          usage: "60% paper, 30% ink, 10% terracotta. No purple, no gradient.",
          css: ":root { --paper: #fdfcfa; --ink: #121212; --hairline: #e8e3dc; --accent: #c45a3c; --radius: 0px; }"
        };
      }
      
      try {
        const {h,s,l} = rgbToHsl(...Object.values(hexToRgb(base)));
        const harmonies = [h, (h+30)%360, (h+180)%360].map(hue => hslToHex(hue, s, l));
        return {
          base_color: base,
          harmony: "analogous + complementary",
          colors: harmonies,
          tints: [1,2,3].map(i => hslToHex(h, s, Math.min(95, l+i*12))),
          shades: [1,2,3].map(i => hslToHex(h, s, Math.max(8, l-i*12))),
          css_variables: harmonies.map((c,i) => `--color-${i}: ${c};`).join('\n'),
          note: "No purple gradient. Single accent, paper base."
        };
      } catch(e) {
        return { error: e.message };
      }
    }
  },

  contrast: {
    name: "check_color_contrast",
    controls: `
      <div class="control-group">
        <label>Foreground (text)</label>
        <input id="fg" class="input" value="#fdfcfa">
      </div>
      <div class="control-group">
        <label>Background</label>
        <input id="bg" class="input" value="#121212">
      </div>
      <button class="btn btn-primary" onclick="runTool('contrast')">Check Contrast —</button>
    `,
    run: () => {
      const fg = document.getElementById('fg')?.value || '#fdfcfa';
      const bg = document.getElementById('bg')?.value || '#121212';
      const ratio = contrastRatio(fg, bg);
      return {
        foreground: fg,
        background: bg,
        ratio: Math.round(ratio*100)/100,
        wcag: {
          AA_normal: ratio >= 4.5,
          AA_large: ratio >= 3,
          AAA_normal: ratio >= 7,
          AAA_large: ratio >= 4.5
        },
        recommendation: ratio >= 7 ? "Excellent - AAA" : ratio >= 4.5 ? "Good - AA" : "Poor - Increase contrast",
        sophisticated_pair: ratio >= 4.5 ? "✓ This pair works for refined UI" : "✗ Avoid - fails AA"
      };
    }
  },

  typography: {
    name: "suggest_typography_pairing",
    controls: `
      <div class="control-group">
        <label>Mood</label>
        <select id="typoMood" class="input" style="border: 0.5px solid var(--hairline); padding: 0 12px;">
          <option value="editorial">editorial — 脱AIにセリフ</option>
          <option value="paper_ink">paper_ink — Paper & Ink</option>
          <option value="japanese">japanese — 日本語洗練</option>
          <option value="grotesk">grotesk — 同一ファミリーで勝負</option>
        </select>
      </div>
      <button class="btn btn-primary" onclick="runTool('typography')">Suggest —</button>
    `,
    run: () => {
      const mood = document.getElementById('typoMood')?.value || 'editorial';
      const pairings = {
        editorial: {
          heading: "Instrument Serif",
          body: "Inter Tight",
          mono: "Fragment Mono",
          reason: "セリフの個性 + サンセリフの中立。AIっぽいInterだけを避ける",
          scale: "Heading 64px, line-height 0.95, tracking -0.03em, weight 400. Body 15px, 1.7.",
          css: "@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif&family=Inter+Tight:wght@400;500&family=Fragment+Mono&display=swap');"
        },
        paper_ink: {
          heading: "Instrument Serif",
          body: "Suisse Int'l / Inter Tight",
          mono: "Fragment Mono",
          reason: "紙とインクに合う、クラシックで読みやすい",
          scale: "Heading 48-88px serif, Body 15px sans, Mono 12px uppercase"
        },
        japanese: {
          heading: "Shippori Mincho",
          body: "Noto Sans JP",
          mono: "IBM Plex Mono",
          reason: "明朝の品格。ゴシックだけの無難さを避ける",
          scale: "日本語は欧文より1.1倍大きく、行間1.8-2.0"
        },
        grotesk: {
          heading: "Neue Haas Grotesk",
          body: "Neue Haas Grotesk",
          mono: "Mono",
          reason: "同一ファミリーでウェイトとサイズで階層。最も洗練",
          scale: "全て同じフォント、400と500だけ。Boldは使わない"
        }
      };
      return pairings[mood] || pairings.editorial;
    }
  }
};

// Default to sophisticated
let currentTool = 'sophisticated';

function renderControls(toolKey) {
  const tool = tools[toolKey];
  if (!tool) return;
  document.getElementById('controls').innerHTML = tool.controls;
  document.getElementById('configDisplay').innerHTML = `Tool: ${tool.name}<br>No purple, no 24px, no shadow<br>Paper #fdfcfa / Ink #121212`;
}

function runTool(toolKey) {
  const tool = tools[toolKey] || tools.sophisticated;
  const result = tool.run();
  document.getElementById('output').textContent = JSON.stringify(result, null, 2);
  
  // Update visual preview for sophisticated
  if (toolKey === 'sophisticated') {
    const preview = document.getElementById('visualPreview');
    preview.innerHTML = `
      <p class="mono" style="margin-bottom: 16px;">Visual Preview — ${result.aesthetic}</p>
      <div style="display: flex; gap: 8px; margin-bottom: 16px;">
        ${Object.entries(result.palette.colors).map(([name, color]) => `
          <div style="flex: 1; height: 48px; background: ${color}; border: 0.5px solid var(--hairline); display: flex; align-items: flex-end; padding: 4px;">
            <span style="font-family: var(--font-mono); font-size: 8px; background: var(--paper); padding: 1px 3px;">${name}</span>
          </div>
        `).join('')}
      </div>
      <div style="display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 16px;">
        <button class="btn btn-primary">Primary — 0px</button>
        <button class="btn btn-secondary">Secondary — Hairline</button>
        <span style="border-bottom: 0.5px solid var(--ink); padding-bottom: 2px; font-size: 13px; cursor: pointer;">Tertiary Underline</span>
      </div>
      <p class="mono" style="font-size: 10px;">${result.css_variables.slice(0, 200)}...</p>
    `;
  }
}

function copyOutput() {
  const text = document.getElementById('output').textContent;
  navigator.clipboard.writeText(text);
  const btn = document.querySelector('button[onclick="copyOutput()"]');
  const orig = btn.textContent;
  btn.textContent = 'Copied —';
  setTimeout(() => btn.textContent = orig, 1000);
}

// Init
document.addEventListener('DOMContentLoaded', () => {
  // Tool nav click
  document.querySelectorAll('#toolNav li').forEach(li => {
    li.addEventListener('click', () => {
      document.querySelectorAll('#toolNav li').forEach(l => l.classList.remove('active'));
      li.classList.add('active');
      currentTool = li.dataset.tool;
      renderControls(currentTool);
      // Auto run
      setTimeout(() => runTool(currentTool), 100);
    });
  });
  
  renderControls('sophisticated');
  setTimeout(() => runTool('sophisticated'), 100);
});
