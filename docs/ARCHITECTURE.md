# Architecture

## Overview

`openmcpart` is a Python MCP server for design-system generation and review. It also includes a read-only local CLI for static HTML/CSS project inspection. The MCP server has **18 tools, 4 resources, and 3 prompts**.

## Package layout

```text
src/openmcpart/
├── server.py                 # MCP registration, transports, audit/tokens CLI
├── tools/
│   ├── accessibility.py      # Accessibility checklist, heuristic critique, components
│   ├── branding.py           # Brand principles and moodboard brief
│   ├── colors.py             # Palette, contrast and gradient helpers
│   ├── layout.py              # Layout and spacing suggestions
│   ├── project_audit.py      # Read-only HTML/CSS audit and token extraction
│   ├── tokens.py              # CSS, Tailwind, JSON and DTCG-style token output
│   ├── typography.py          # Font pairing and type scales
│   └── ui_generator.py        # Optional Paper & Ink / editorial aesthetics
└── utils/
    └── color_utils.py         # Color conversion, WCAG contrast and color-blind simulation
```

## MCP surface

### 18 tools

- **Color:** `generate_color_palette`, `check_color_contrast`, `generate_gradient`
- **Typography:** `suggest_typography_pairing`, `generate_type_scale`
- **Layout:** `suggest_layout`, `generate_spacing_system`
- **Design tokens:** `generate_design_tokens`, `generate_tailwind_config`, `extract_project_tokens`
- **Accessibility and review:** `check_accessibility`, `critique_design`, `suggest_component_variants`, `audit_project`
- **Branding:** `extract_design_principles`, `generate_moodboard_brief`
- **Style direction:** `generate_sophisticated_ui`, `critique_ai_look`

### Resources and prompts

- Resources: `design://tokens/template`, `design://guidelines/8pt-grid`, `design://guidelines/wcag`, `design://checklist/design-review`
- Prompts: `design_critique_prompt`, `branding_workshop_prompt`, `component_design_prompt`

## Transports and CLI

- **stdio** is the default for MCP clients.
- **SSE** and **streamable HTTP** can be selected with `--transport` or `MCP_TRANSPORT`; HTTP binds to loopback by default (`127.0.0.1`). Set `MCP_HOST=0.0.0.0` only when a container or trusted network boundary requires it.
- `openmcpart audit <directory>` prints a static audit report.
- `openmcpart tokens <directory>` extracts local CSS token candidates.
- Both CLI commands support `--format markdown|json` and `--max-files`.
- `audit` also supports `--fail-on none|low|medium|high|critical` for CI.
- The root `action.yml` defines a composite GitHub Action; its default threshold is `high`, and it writes a Markdown report to the step summary and exposes its path as `report`.

Example workflow step inside this repository:

```yaml
- uses: ./
  with:
    project-path: .
    fail-on: high
```

The Composite Action definition is covered by static review but has not yet been exercised on GitHub-hosted runners.

## Project audit safety and scope

`audit_project` and `extract_project_tokens` require a path argument from MCP callers; the CLI defaults to the current directory only when explicitly invoked without a path. The scanner:

- reads supported text files only; it does not execute project code;
- makes no network requests and never writes to the scanned project;
- does not follow symlinks;
- skips hidden/generated/dependency directories and files larger than 1 MB;
- reads at most 20 MB total per scan;
- defaults to a 500-file limit (up to 5,000 can be requested);
- returns relative source locations and heuristic findings.

Markup semantics are parsed from `.html` and `.htm`; CSS is read from `.css` and `<style>` blocks in `.vue` / `.svelte` files. Checks cover missing document language and title, image alt attributes, names for buttons and links (including linked image alt text), form labels, duplicate IDs, skipped heading levels, missing `aria-labelledby` references, some same-rule CSS contrast pairs, removed focus outlines, and motion preferences. Token extraction reports CSS custom properties, repeated colors, font families, spacing values, radii, and shadows. Returned custom properties are capped at 500, color tokens at 200, and individual token values at 500 characters; truncation is reported in the JSON result.

This is **not** a browser renderer, a screen-reader test, or a WCAG conformance certificate. CSS inheritance, runtime-generated markup, opacity, images behind text, layout geometry, and many framework-specific patterns require browser or manual verification. Reports explicitly include these limitations.

## Design principles

1. Keep the core deterministic and local; no external AI API key is required.
2. Keep file inspection read-only and opt-in through an explicit project path.
3. Distinguish measured values from heuristic suggestions and manual checks.
4. Prefer outputs that developers can review and adapt; do not imply that a style preference is a universal quality rule.
5. Keep MCP tool schemas small, typed, and independently testable.

## Dependencies

Runtime dependencies are `mcp` and `pydantic`. The project audit uses Python's standard library. Development dependencies are available through `pip install -e '.[dev]'`.

## Testing and linting

```bash
pip install -e '.[dev]'
ruff check src tests
pytest -q
```

CI runs the lint, tests, package installation, and local audit CLI on Python 3.10–3.13.
