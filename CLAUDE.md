# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the portfolio locally
python app.py

# Install Python dependencies
pip install -r requirements.txt
```

The app runs on port 8080 by default, or the `$PORT` environment variable if set. NiceGUI's `reload=True` is active — the server auto-restarts on file changes.

The `package.json` / `npm run dev` (Vite) exist in the repo but are **not used** by the app. Ignore them.

## Architecture

This is a **personal portfolio website** (bilingual FR/EN) served as a single monolithic HTML page. The entire backend is `app.py` (~880 lines). There is no frontend framework and no template engine.

### Core flow

`app.py` has one route (`GET /`) that reads `?lang=fr|en` and calls `_build_page(lang)`. That function assembles a complete HTML document by concatenating Python f-strings and returns it via FastAPI's `HTMLResponse`. NiceGUI is used only as the server wrapper (`ui.run()`).

### How HTML is built

All HTML is constructed **inline in `_build_page()`** using Python f-strings — there is no template engine, no `$varname` substitution, and no external template files. The function:

1. Computes bilingual labels with inline `if fr else` ternaries (no `I18N` dict).
2. Builds each section as a string (navbar, intro, about, skills, experience, projects, alternance, cv, contact).
3. Concatenates them with a `sec(anchor, content)` helper that wraps content in `<section id="...">`.
4. Returns `head + navbar + intro + sec(...) * N + footer + scripts`.

### CSS and theming

A single `_CSS` string (defined at module level) contains all styles including a `:root { --bg; --card; --text; --muted; --border; --accent; --green; --amber; --purple; }` palette. Light/dark mode is toggled client-side via `data-theme` attribute + `localStorage`, using `toggleTheme()` in the inline JS.

### PDF / CV

`_get_pdf_b64(filename)` reads PDFs from `assets/` and base64-encodes them (LRU-cached). Both FR and EN CVs are embedded as data URIs for inline viewing (rendered page-by-page via pdf.js from a CDN) and direct download.

### The `templates/` directory

The `templates/` folder contains `.html` fragments that are **not imported or used** in the current `app.py`. They appear to be legacy files from a previous version of the site.

### Static assets

`assets/` is mounted at `/assets`. It contains favicons, CV PDFs, and images. PDFs are also base64-embedded at runtime (see above).
