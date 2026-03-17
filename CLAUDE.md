# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the portfolio locally
python app.py

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies (Vite, for frontend asset work)
npm install

# Run Vite dev server (if working on frontend assets)
npm run dev
```

The app runs on port 8080 by default, or the `$PORT` environment variable if set.

## Architecture

This is a **personal portfolio website** (bilingual FR/EN) built with NiceGUI/FastAPI as the backend. There is no frontend framework — the server dynamically assembles a full monolithic HTML page from template fragments and serves it.

### Core flow

`app.py` is the entire backend. A single route (`GET /`) accepts `?lang=en|fr` and calls `_build_page(lang)`, which:
1. Loads HTML fragments from `templates/` via string substitution
2. Injects theme CSS variables from the `THEME` dict
3. Renders interactive Plotly charts (skills radar, bar chart, Sankey, timeline) inline
4. Returns a complete HTML document via `nicegui.ui.html()`

### Templates

- `templates/` holds HTML fragments (28 files). French is the default; English versions follow the `*_en.html` naming convention.
- Template variables use `$varname` syntax, replaced at runtime with theme colors and translated strings.
- The `I18N` dict in `app.py` holds all UI string translations.

### Theme system

A central `THEME` dict in `app.py` defines the full color palette. These are injected as CSS custom properties into the page. Light/dark mode is toggled client-side via JS with `localStorage` persistence.

### Static assets

`assets/` is mounted at `/assets`. PDFs (CVs) are also base64-encoded at runtime with LRU caching and embedded as data URIs for inline browser viewing.
