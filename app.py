import base64
import os
from functools import lru_cache
from pathlib import Path
from string import Template

import plotly.graph_objects as go
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from nicegui import app as nicegui_app, ui
from plotly.subplots import make_subplots

THEME = {
    "accent":       "#2563EB",
    "accent_light": "#60A5FA",
    "bg":           "#0A0A0F",
    "card":         "#111118",
    "card_alt":     "#16161F",
    "text":         "#F0F0F5",
    "muted":        "#6B6B80",
    "border":       "rgba(255,255,255,0.06)",
    "green":        "#10B981",
    "amber":        "#F59E0B",
    "purple":       "#A855F7",
    "purple_light": "#C084FC",
}

TEMPLATES_DIR = Path(__file__).parent / "templates"
ASSETS_DIR    = Path(__file__).parent / "assets"

nicegui_app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")


def _normalize_lang(value: str | None) -> str:
    return "FR" if str(value).lower() == "fr" else "EN"


def load(filename: str, lang: str | None = None) -> str:
    path = TEMPLATES_DIR / filename
    if _normalize_lang(lang) == "EN":
        en_path = path.with_name(f"{path.stem}_en{path.suffix}")
        if en_path.exists():
            path = en_path
    return path.read_text(encoding="utf-8")


def T(raw: str) -> str:
    return Template(raw).safe_substitute(THEME)


_BASE_CSS = T(load("base.css"))


@lru_cache(maxsize=10)
def _get_pdf_b64(filename: str) -> str:
    return base64.b64encode((ASSETS_DIR / filename).read_bytes()).decode()


I18N = {
    "EN": {
        "radar_level":          "Level",
        "radar_title":          "Overview",
        "bar_title":            "By Domain",
        "alt_months": [
            "Sep 26", "Oct", "Nov", "Dec", "Jan 27",
            "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep 27",
        ],
        "alt_company":          "Company",
        "alt_school":           "School",
        "alt_time_axis":        "% of time",
        "alt_annotation_month": "Apr",
        "alt_annotation_text":  "🟢 100% company from April",
        "disclaimer": (
            "These scores reflect my own honest assessment"
            " — rated on a scale of 0 to 100 based on my experience."
        ),
    },
    "FR": {
        "radar_level":          "Niveau",
        "radar_title":          "Vue d'ensemble",
        "bar_title":            "Par domaine",
        "alt_months": [
            "Sept 26", "Oct", "Nov", "Déc", "Jan 27",
            "Fév", "Mar", "Avr", "Mai", "Juin",
            "Juil", "Août", "Sept 27",
        ],
        "alt_company":          "Entreprise",
        "alt_school":           "École",
        "alt_time_axis":        "% du temps",
        "alt_annotation_month": "Avr",
        "alt_annotation_text":  "🟢 100% entreprise dès avril",
        "disclaimer": (
            "Ces scores reflètent mon auto-évaluation honnête"
            " — notés sur une échelle de 0 à 100 selon mon expérience."
        ),
    },
}


def _build_page(lang: str) -> str:
    TXT = I18N[lang]

    RADAR_CATEGORIES = [
        "Python", "SQL", "JavaScript",
        "React", "Next.js", "Node.js",
        "Docker", "Git", "LLMs", "PostgreSQL",
    ]
    RADAR_VALUES = [70, 75, 80, 80, 78, 75, 65, 75, 25, 75]

    _k_data = "Data & AI"      if lang == "EN" else "Data & IA"
    _k_lang = "Core Languages" if lang == "EN" else "Langages"
    _k_fw   = "Frameworks & Tools"
    _k_ops  = "Platform & Ops"

    SKILL_GROUPS = {
        _k_lang: {"Python": 70, "SQL": 75, "JavaScript": 80},
        _k_fw:   {"Node.js": 75, "Symfony": 65, "React": 80, "Next.js": 78},
        _k_ops:  {"Docker": 65, "Git": 75, "Bash": 65, "VMWare": 60},
        _k_data: {"LLMs": 25, "PostgreSQL": 75, "NoSQL": 75},
    }

    GROUP_COLORS = {
        _k_lang: THEME["accent"],
        _k_fw:   THEME["green"],
        _k_ops:  THEME["amber"],
        _k_data: THEME["purple"],
    }

    _cfg = {"displayModeBar": False, "responsive": True}

    fig_skills = make_subplots(
        rows=1, cols=2,
        specs=[[{"type": "polar"}, {"type": "xy"}]],
        column_widths=[0.34, 0.66],
        horizontal_spacing=0.34,
        subplot_titles=[TXT["radar_title"], TXT["bar_title"]],
    )

    fig_skills.add_trace(go.Scatterpolar(
        r=RADAR_VALUES + [RADAR_VALUES[0]],
        theta=RADAR_CATEGORIES + [RADAR_CATEGORIES[0]],
        fill="toself",
        fillcolor="rgba(37,99,235,0.12)",
        line=dict(color=THEME["accent"], width=2),
        marker=dict(size=6, color=THEME["accent_light"]),
        hovertemplate=f"<b>%{{theta}}</b><br>{TXT['radar_level']}: %{{r}}/100<extra></extra>",
        showlegend=False,
    ), row=1, col=1)

    _bar_skills, _bar_values, _bar_colors = [], [], []
    for group_name, items in SKILL_GROUPS.items():
        for skill, value in items.items():
            _bar_skills.append(skill)
            _bar_values.append(value)
            _bar_colors.append(GROUP_COLORS[group_name])

    fig_skills.add_trace(go.Bar(
        y=_bar_skills,
        x=_bar_values,
        orientation="h",
        marker=dict(color=_bar_colors),
        hovertemplate="<b>%{y}</b>: %{x}/100<extra></extra>",
        showlegend=False,
    ), row=1, col=2)

    for group_name in SKILL_GROUPS:
        fig_skills.add_trace(go.Bar(
            y=[], x=[], name=group_name, orientation="h",
            marker=dict(color=GROUP_COLORS[group_name]),
        ), row=1, col=2)

    fig_skills.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=60, b=70),
        height=520,
        font=dict(family="Space Grotesk", color="#8888A0", size=11),
        bargap=0.55,
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True, range=[0, 100],
                gridcolor="rgba(255,255,255,0.04)",
                tickfont=dict(size=9, color=THEME["muted"]),
            ),
            angularaxis=dict(
                gridcolor="rgba(255,255,255,0.06)",
                tickfont=dict(size=11, color=THEME["text"], family="Inter"),
            ),
        ),
        xaxis2=dict(
            range=[0, 100],
            gridcolor="rgba(255,255,255,0.06)",
            tickfont=dict(color=THEME["muted"], size=10),
            zeroline=False,
            fixedrange=True,
        ),
        yaxis2=dict(
            autorange="reversed",
            tickfont=dict(color=THEME["text"], size=11),
            tickmode="linear",
            automargin=True,
            fixedrange=True,
        ),
        dragmode=False,
        legend=dict(
            orientation="h", y=-0.15, x=0.80, xanchor="center",
            font=dict(size=11, color=THEME["muted"]),
            bgcolor="rgba(0,0,0,0)",
        ),
        shapes=[dict(
            type="line",
            xref="paper", yref="paper",
            x0=0.45, x1=0.45, y0=0.02, y1=0.98,
            line=dict(color="rgba(255,255,255,0.09)", width=1, dash="dot"),
        )],
    )
    fig_skills.update_annotations(font_color=THEME["muted"], font_size=13)

    skills_div = fig_skills.to_html(
        full_html=False, include_plotlyjs="cdn",
        config={"displayModeBar": False, "responsive": True, "staticPlot": False},
    )

    _sankey_roles = (
        ["User", "UI", "API", "Storage", "AI", "Infra"]
        if lang == "EN" else
        ["Utilisateur", "Interface", "API", "Stockage", "IA", "Infra"]
    )
    fig_sankey = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(
            pad=22, thickness=22,
            line=dict(color="rgba(37,99,235,0.3)", width=1),
            label=[
                "Client / Browser",
                "Next.js · React",
                "Node.js · Symfony",
                "PostgreSQL · NoSQL",
                "Python · LLMs",
                "Docker · Git",
            ],
            color=[THEME["card_alt"]] * 6,
            customdata=_sankey_roles,
            hovertemplate="%{label}<br><i>%{customdata}</i><extra></extra>",
        ),
        link=dict(
            source=[0, 1, 2, 2, 3, 4],
            target=[1, 2, 3, 4, 5, 5],
            value=[10, 10, 6, 4, 4, 4],
            color=[
                "rgba(37,99,235,0.15)",
                "rgba(37,99,235,0.15)",
                "rgba(16,185,129,0.15)",
                "rgba(168,85,247,0.15)",
                "rgba(245,158,11,0.15)",
                "rgba(245,158,11,0.15)",
            ],
            hovertemplate="%{source.label} → %{target.label}<extra></extra>",
        ),
    ))
    fig_sankey.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Grotesk", color="#8888A0", size=12),
        margin=dict(l=20, r=20, t=10, b=10),
        height=200,
    )
    sankey_div = fig_sankey.to_html(full_html=False, include_plotlyjs=False, config=_cfg)

    MONTHS     = TXT["alt_months"]
    ENTREPRISE = [33, 33, 33, 33, 33, 33, 33, 100, 100, 100, 100, 100, 100]
    ECOLE      = [67, 67, 67, 67, 67, 67, 67,   0,   0,   0,   0,   0,   0]
    fig_alt = go.Figure()
    fig_alt.add_trace(go.Bar(
        x=MONTHS, y=ENTREPRISE, name=TXT["alt_company"],
        marker=dict(color=THEME["accent"]),
        hovertemplate=f"%{{x}}<br><b>{TXT['alt_company']}</b>: %{{y}}%<extra></extra>",
    ))
    fig_alt.add_trace(go.Bar(
        x=MONTHS, y=ECOLE, name=TXT["alt_school"],
        marker=dict(color="rgba(255,255,255,0.08)"),
        hovertemplate=f"%{{x}}<br><b>{TXT['alt_school']}</b>: %{{y}}%<extra></extra>",
    ))
    fig_alt.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color=THEME["text"], size=11),
        margin=dict(l=40, r=20, t=30, b=40),
        height=260,
        xaxis=dict(
            tickfont=dict(size=10, color=THEME["muted"]),
            gridcolor="rgba(255,255,255,0.03)",
        ),
        yaxis=dict(
            title=dict(text=TXT["alt_time_axis"], font=dict(size=10, color=THEME["muted"])),
            ticksuffix="%",
            range=[0, 108],
            gridcolor="rgba(255,255,255,0.04)",
            tickfont=dict(size=10, color=THEME["muted"]),
        ),
        legend=dict(
            orientation="h", y=1.15, x=0.5, xanchor="center",
            font=dict(size=11, color=THEME["muted"]),
            bgcolor="rgba(0,0,0,0)",
        ),
        annotations=[dict(
            x=TXT["alt_annotation_month"], y=107,
            text=TXT["alt_annotation_text"],
            showarrow=False,
            font=dict(size=10, color=THEME["green"]),
        )],
    )
    alt_div = fig_alt.to_html(full_html=False, include_plotlyjs=False, config=_cfg)

    def tpl(name: str, extra: dict | None = None) -> str:
        return Template(load(name, lang=lang)).safe_substitute({**THEME, **(extra or {})})

    _lang_vars = {
        "lang_en_class": "lang-active" if lang == "EN" else "",
        "lang_fr_class": "lang-active" if lang == "FR" else "",
    }
    navbar        = tpl("navbar.html", _lang_vars)
    hero          = tpl("hero.html")
    presentation  = tpl("presentation.html")
    skills_header = tpl("skills_header.html")
    projects         = tpl("projects.html")
    personal_projects = tpl("personal_projects.html")
    sankey_label  = tpl("sankey_label.html")
    experiences   = tpl("experiences.html")
    alt_header    = tpl("alternance_header.html")
    alt_banner    = tpl("alternance_banner.html")
    cv            = tpl("cv.html", {
        "pdf_fr": _get_pdf_b64("CV_IBRAHIM_2026.pdf"),
        "pdf_en": _get_pdf_b64("CV_Ibrahim_Kara_en.pdf"),
    })
    contact_file  = "CV_Ibrahim_Kara_en.pdf" if lang == "EN" else "CV_IBRAHIM_2026.pdf"
    contact_name  = "CV_Ibrahim_Kara_en.pdf" if lang == "EN" else "CV_Ibrahim_Karamanlian_FR.pdf"
    contact       = tpl("contact.html", {
        "cv_download_href": "data:application/pdf;base64," + _get_pdf_b64(contact_file),
        "cv_download_name": contact_name,
    })

    global_css = (
        "body,html{margin:0;padding:0;}"
        "body{"
        "background-color:var(--bg);"
        "background-image:"
        "linear-gradient(var(--rect-line) 1px,transparent 1px),"
        "linear-gradient(90deg,var(--rect-line) 1px,transparent 1px),"
        "linear-gradient(var(--rect-line-bold) 1px,transparent 1px),"
        "linear-gradient(90deg,var(--rect-line-bold) 1px,transparent 1px);"
        "background-size:60px 60px,60px 60px,300px 300px,300px 300px;"
        "background-attachment:fixed;}"
        "::-webkit-scrollbar{width:5px;}"
        "::-webkit-scrollbar-track{background:var(--bg);}"
        "::-webkit-scrollbar-thumb{background:#2563EB;border-radius:3px;}"
        ".section-anchor{display:block;position:relative;top:-12px;visibility:hidden;height:0;}"
        ".navbar{background:var(--navbar-bg)!important;}"
        "[data-theme='light'] .navbar{border-bottom-color:rgba(0,0,0,0.07)!important;}"
        "[data-theme='light'] .nav-lang{border-left-color:rgba(0,0,0,0.12)!important;}"
        "[data-theme='light'] .nav-lang-sep{color:rgba(0,0,0,0.2)!important;}"
        "[data-theme='light'] .nav-links a:hover{background:rgba(0,0,0,0.05)!important;}"
        ".skills-wrap{background:var(--card-alt);border-top:1px solid var(--border);border-bottom:1px solid var(--border);padding:4rem 0 3rem;}"
        ".chart-wrap{width:100%;max-width:1200px;margin:1.5rem auto 0;padding:0 2.5rem;box-sizing:border-box;}"
        "[data-theme='light'] .js-plotly-plot svg text{fill:#2d2d3a!important;}"
        "[data-theme='light'] .js-plotly-plot .gridlayer path{stroke:rgba(0,0,0,0.09)!important;}"
        "[data-theme='light'] .js-plotly-plot .angularaxis .angulartick text{fill:#2d2d3a!important;}"
        "[data-theme='light'] .js-plotly-plot .radialaxis line{stroke:rgba(0,0,0,0.09)!important;}"
        "[data-theme='light'] .js-plotly-plot .angular-line{stroke:rgba(0,0,0,0.12)!important;}"
        ".skills-disclaimer{text-align:center;color:var(--muted);font-size:0.79rem;font-style:italic;"
        "margin:1.6rem auto 0;max-width:700px;padding:1rem 2rem 0;"
        "border-top:1px solid var(--border);font-family:'Space Grotesk',sans-serif;line-height:1.6;}"
        ".js-plotly-plot .plotly .modebar{display:none!important;}"
        ".theme-toggle{width:32px;height:32px;border-radius:50%;border:1.5px solid var(--border);"
        "background:transparent;cursor:pointer;display:flex;align-items:center;justify-content:center;"
        "color:var(--muted);transition:all 0.2s;font-size:15px;margin-right:4px;padding:0;}"
        ".theme-toggle:hover{color:var(--text);border-color:var(--accent);}"
        "@media(max-width:680px){"
        ".chart-wrap{padding:0;margin-top:1rem;overflow-x:auto;-webkit-overflow-scrolling:touch;}"
        ".chart-wrap .js-plotly-plot{min-width:620px;}"
        ".skills-wrap{padding:2.5rem 0 2rem;}"
        ".skills-disclaimer{margin:1.2rem 1.2rem 0;padding:0.8rem 1rem 0;font-size:0.75rem;}"
        ".theme-toggle{display:none;}"
        ".section-title{font-size:clamp(26px,7vw,40px)!important;}"
        ".section-desc{font-size:13px!important;}"
        "}"
    )

    disclaimer_html = f'<p class="skills-disclaimer">{TXT["disclaimer"]}</p>'

    parts = [
        "<!DOCTYPE html>",
        f'<html lang="{lang.lower()}">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>Ibrahim Karamanlian | Data Engineer</title>",
        '<script>!function(){var t=localStorage.getItem("theme")||"dark";document.documentElement.setAttribute("data-theme",t)}();</script>',
        '<link rel="apple-touch-icon" sizes="57x57" href="/assets/apple-icon-57x57.png">',
        '<link rel="apple-touch-icon" sizes="60x60" href="/assets/apple-icon-60x60.png">',
        '<link rel="apple-touch-icon" sizes="72x72" href="/assets/apple-icon-72x72.png">',
        '<link rel="apple-touch-icon" sizes="76x76" href="/assets/apple-icon-76x76.png">',
        '<link rel="apple-touch-icon" sizes="114x114" href="/assets/apple-icon-114x114.png">',
        '<link rel="apple-touch-icon" sizes="120x120" href="/assets/apple-icon-120x120.png">',
        '<link rel="apple-touch-icon" sizes="144x144" href="/assets/apple-icon-144x144.png">',
        '<link rel="apple-touch-icon" sizes="152x152" href="/assets/apple-icon-152x152.png">',
        '<link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-icon-180x180.png">',
        '<link rel="icon" type="image/png" sizes="192x192" href="/assets/android-icon-192x192.png">',
        '<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32x32.png">',
        '<link rel="icon" type="image/png" sizes="96x96" href="/assets/favicon-96x96.png">',
        '<link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16x16.png">',
        '<link rel="manifest" href="/assets/manifest.json">',
        '<meta name="msapplication-TileColor" content="#0A0A0F">',
        '<meta name="msapplication-TileImage" content="/assets/ms-icon-144x144.png">',
        '<meta name="theme-color" content="#0A0A0F">',
        f"<style>{_BASE_CSS}</style>",
        f"<style>{global_css}</style>",
        "</head>",
        "<body>",
        navbar,
        '<span id="home" class="section-anchor"></span>',
        hero,
        presentation,
        '<span id="skills" class="section-anchor"></span>',
        '<div class="skills-wrap">',
        skills_header,
        '<div class="chart-wrap">',
        skills_div,
        '</div>',
        disclaimer_html,
        "</div>",
        '<span id="projects" class="section-anchor"></span>',
        projects,
        personal_projects,
        sankey_label,
        f'<div class="chart-wrap">{sankey_div}</div>',
        '<span id="experience" class="section-anchor"></span>',
        experiences,
        '<span id="alternance" class="section-anchor"></span>',
        alt_header,
        f'<div class="chart-wrap">{alt_div}</div>',
        alt_banner,
        '<span id="cv" class="section-anchor"></span>',
        cv,
        '<span id="contact" class="section-anchor"></span>',
        contact,
        "<script>",
        "function toggleTheme(){",
        "  var t=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';",
        "  document.documentElement.setAttribute('data-theme',t);",
        "  localStorage.setItem('theme',t);",
        "  var b=document.getElementById('theme-btn');",
        "  if(b)b.textContent=t==='dark'?'◑':'◐';",
        "}",
        "document.addEventListener('DOMContentLoaded',function(){",
        "  var b=document.getElementById('theme-btn');",
        "  if(b){var t=localStorage.getItem('theme')||'dark';b.textContent=t==='dark'?'◑':'◐';}",
        "});",
        "</script>",
        "</body>",
        "</html>",
    ]
    return "\n".join(parts)


@nicegui_app.get("/")
async def index(request: Request):
    lang = "FR" if request.query_params.get("lang", "en").lower() == "fr" else "EN"
    return HTMLResponse(content=_build_page(lang))


ui.run(
    title="Ibrahim Karamanlian | Data Engineer",
    favicon="/assets/MOI_Icon.png",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 8080)),
    dark=True,
    reload=False,
    show=False,
)
