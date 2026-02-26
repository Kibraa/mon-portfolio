"""
╔══════════════════════════════════════════════════════════════╗
║  Ibrahim KARAMANLIAN — Data Engineering & IA Portfolio       ║
║  Stack: Streamlit · Plotly · Python                          ║
║  Deploy: streamlit run app.py                                ║
╠══════════════════════════════════════════════════════════════╣
║  Architecture:                                               ║
║    templates/base.css              → CSS partagé             ║
║    templates/streamlit_overrides   → overrides Streamlit     ║
║    templates/navbar.html           → barre de navigation     ║
║    templates/hero.html             → section héro            ║
║    templates/skills_header.html    → en-tête compétences     ║
║    templates/projects.html         → projets piliers         ║
║    templates/sankey_label.html     → label du diagramme      ║
║    templates/experiences.html      → parcours professionnel  ║
║    templates/alternance_header.html→ en-tête alternance      ║
║    templates/alternance_banner.html→ bannière alternance     ║
║    templates/contact.html          → contact + footer        ║
║                                                              ║
║  Variables CSS: syntaxe $var (string.Template)               ║
║  → Aucune f-string, aucun {{ }}, VS Code 100% stable.       ║
╚══════════════════════════════════════════════════════════════╝
"""

from pathlib import Path
from string import Template

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONFIG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="Ibrahim Karamanlian | Data Engineer",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# THEME — single source of truth
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TEMPLATES_DIR = Path(__file__).parent / "templates"


def _normalize_lang(value: str | None) -> str:
    return "FR" if str(value).lower() == "fr" else "EN"


def load(filename: str, lang: str | None = None) -> str:
    """Lit un template avec fallback FR si la variante EN n'existe pas."""
    path = TEMPLATES_DIR / filename
    if _normalize_lang(lang) == "EN":
        en_path = path.with_name(f"{path.stem}_en{path.suffix}")
        if en_path.exists():
            path = en_path
    return path.read_text(encoding="utf-8")


def T(raw: str) -> str:
    """Remplace les $variables par les valeurs du THEME."""
    return Template(raw).safe_substitute(THEME)


# Cache le CSS de base (lu une seule fois)
_BASE_CSS = T(load("base.css"))


def render_html(template_name: str, height: int = 600, lang: str = "FR") -> None:
    """Charge un template HTML, injecte le thème, rend via iframe."""
    body = T(load(template_name, lang=lang))
    doc = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<style>" + _BASE_CSS + "</style>"
        "</head><body>" + body
        + (
            "<script>"
            "const sendHeight=()=>{"
            "const h=Math.max(document.body.scrollHeight,document.documentElement.scrollHeight);"
            "window.parent.postMessage({isStreamlitMessage:true,type:'streamlit:setFrameHeight',height:h},'*');"
            "};"
            "window.addEventListener('load',sendHeight);"
            "new ResizeObserver(sendHeight).observe(document.body);"
            "setTimeout(sendHeight,50);setTimeout(sendHeight,250);setTimeout(sendHeight,800);"
            "</script>"
        )
        + "</body></html>"
    )
    components.html(doc, height=height, scrolling=False)


def render_inline(template_name: str, lang: str = "FR") -> None:
    """Rend un template directement dans le DOM Streamlit (sans iframe)."""
    st.markdown(T(load(template_name, lang=lang)), unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STREAMLIT OVERRIDES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(T(load("streamlit_overrides.html")), unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# LANGUAGE SWITCH
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
query_lang = _normalize_lang(st.query_params.get("lang", "en"))
if "lang" not in st.session_state:
    st.session_state.lang = query_lang
else:
    st.session_state.lang = _normalize_lang(st.session_state.lang)

if st.session_state.lang != query_lang:
    st.session_state.lang = query_lang

_, col_lang = st.columns([0.88, 0.12])
with col_lang:
    selected_lang = st.radio(
        "Language",
        options=["EN", "FR"],
        horizontal=True,
        index=0 if st.session_state.lang == "EN" else 1,
        label_visibility="collapsed",
    )

LANG = selected_lang
if st.query_params.get("lang") != LANG.lower():
    st.query_params["lang"] = LANG.lower()

I18N = {
    "EN": {
        "radar_level": "Level",
        "radar_title": "Overview",
        "bar_title": "By Domain",
        "alt_months": [
            "Sep 26", "Oct", "Nov", "Dec", "Jan 27",
            "Feb", "Mar", "Apr", "May", "Jun",
            "Jul", "Aug", "Sep 27",
        ],
        "alt_company": "Company",
        "alt_school": "School",
        "alt_time_axis": "% of time",
        "alt_annotation_month": "Apr",
        "alt_annotation_text": "🟢 100% company from April",
    },
    "FR": {
        "radar_level": "Niveau",
        "radar_title": "Vue d'ensemble",
        "bar_title": "Par domaine",
        "alt_months": [
            "Sept 26", "Oct", "Nov", "Déc", "Jan 27",
            "Fév", "Mar", "Avr", "Mai", "Juin",
            "Juil", "Août", "Sept 27",
        ],
        "alt_company": "Entreprise",
        "alt_school": "École",
        "alt_time_axis": "% du temps",
        "alt_annotation_month": "Avr",
        "alt_annotation_text": "🟢 100% entreprise dès avril",
    },
}
TXT = I18N[LANG]


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# NAVBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
render_inline("navbar.html", lang=LANG)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HERO
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("<div id='home' class='section-anchor'></div>", unsafe_allow_html=True)
render_html("hero.html", height=680, lang=LANG)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SKILLS — Header + Plotly Charts
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("<div id='skills' class='section-anchor'></div>", unsafe_allow_html=True)
render_html("skills_header.html", height=160, lang=LANG)

RADAR_CATEGORIES = [
    "Python", "SQL", "JavaScript", "Docker",
    "CI/CD", "Cloud", "LLMs / RAG", "ETL Pipelines", "Data Viz",
]
RADAR_VALUES = [92, 80, 85, 75, 70, 60, 78, 72, 82]

SKILL_GROUPS = {
    "Engineering":    {"Python": 92, "SQL": 80, "JavaScript/TS": 85, "Java": 55},
    "Infrastructure": {"Docker": 75, "CI/CD": 70, "Cloud (AWS/GCP)": 60, "Kubernetes": 45},
    "Data & AI" if LANG == "EN" else "Data & IA": {
        "LLMs (Claude/RAG)": 78, "ETL Pipelines": 72, "Pandas/NumPy": 76, "Data Viz": 82
    },
}

GROUP_COLORS = {
    "Engineering":    THEME["accent"],
    "Infrastructure": THEME["green"],
    "Data & AI" if LANG == "EN" else "Data & IA": THEME["purple"],
}

col_radar, col_bar = st.columns(2, gap="medium")

with col_radar:
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=RADAR_VALUES + [RADAR_VALUES[0]],
        theta=RADAR_CATEGORIES + [RADAR_CATEGORIES[0]],
        fill="toself",
        fillcolor="rgba(37,99,235,0.12)",
        line=dict(color=THEME["accent"], width=2),
        marker=dict(size=6, color=THEME["accent_light"]),
        hovertemplate=f"<b>%{{theta}}</b><br>{TXT['radar_level']}: %{{r}}/100<extra></extra>",
    ))
    fig_radar.update_layout(
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
        paper_bgcolor=THEME["card_alt"],
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=60, r=60, t=40, b=40),
        height=420,
        font=dict(family="Inter", color=THEME["text"]),
        showlegend=False,
        title=dict(text=TXT["radar_title"], font=dict(size=14, color=THEME["muted"]), x=0.5),
    )
    st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

with col_bar:
    fig_bar = go.Figure()
    for group_name, items in SKILL_GROUPS.items():
        fig_bar.add_trace(go.Bar(
            y=list(items.keys()),
            x=list(items.values()),
            name=group_name,
            orientation="h",
            marker=dict(color=GROUP_COLORS[group_name]),
            hovertemplate="<b>%{y}</b>: %{x}/100<extra></extra>",
        ))
    fig_bar.update_layout(
        barmode="group",
        paper_bgcolor=THEME["card_alt"],
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=20, t=40, b=20),
        height=420,
        font=dict(family="Inter", color=THEME["text"], size=11),
        xaxis=dict(
            range=[0, 100],
            gridcolor="rgba(255,255,255,0.04)",
            tickfont=dict(color=THEME["muted"], size=10),
        ),
        yaxis=dict(
            autorange="reversed",
            tickfont=dict(color=THEME["text"], size=11),
        ),
        legend=dict(
            orientation="h", y=1.08, x=0.5, xanchor="center",
            font=dict(size=11, color=THEME["muted"]),
            bgcolor="rgba(0,0,0,0)",
        ),
        title=dict(text=TXT["bar_title"], font=dict(size=14, color=THEME["muted"]), x=0.5),
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PROJECTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("<div id='projects' class='section-anchor'></div>", unsafe_allow_html=True)
render_html("projects.html", height=620, lang=LANG)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ARCHITECTURE SANKEY
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown(T(load("sankey_label.html", lang=LANG)), unsafe_allow_html=True)

fig_sankey = go.Figure(go.Sankey(
    arrangement="snap",
    node=dict(
        pad=20, thickness=22,
        line=dict(color="rgba(37,99,235,0.3)", width=1),
        label=[
            "App Logs", "Kafka Broker", "Python ETL",
            "PostgreSQL", "Grafana Dashboard", "Alerting",
        ],
        color=[THEME["card_alt"]] * 6,
        customdata=[
            "Source", "Ingestion", "Transform",
            "Storage", "Viz", "Monitoring",
        ],
        hovertemplate="%{label}<br><i>%{customdata}</i><extra></extra>",
    ),
    link=dict(
        source=[0, 1, 2, 3, 3],
        target=[1, 2, 3, 4, 5],
        value=[8, 8, 8, 5, 3],
        color=[
            "rgba(37,99,235,0.15)",
            "rgba(37,99,235,0.15)",
            "rgba(37,99,235,0.15)",
            "rgba(16,185,129,0.15)",
            "rgba(245,158,11,0.15)",
        ],
        hovertemplate="%{source.label} → %{target.label}<extra></extra>",
    ),
))
fig_sankey.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color=THEME["text"], size=12),
    margin=dict(l=20, r=20, t=10, b=10),
    height=200,
)
st.plotly_chart(fig_sankey, use_container_width=True, config={"displayModeBar": False})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EXPERIENCES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("<div id='experience' class='section-anchor'></div>", unsafe_allow_html=True)
render_html("experiences.html", height=820, lang=LANG)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ALTERNANCE — Header + Timeline + Banner
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("<div id='alternance' class='section-anchor'></div>", unsafe_allow_html=True)
render_html("alternance_header.html", height=165, lang=LANG)

MONTHS = TXT["alt_months"]
ENTREPRISE = [60, 60, 60, 60, 60, 60, 60, 100, 100, 100, 100, 100, 100]
ECOLE =      [40, 40, 40, 40, 40, 40, 40,   0,   0,   0,   0,   0,   0]

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
    annotations=[
        dict(
            x=TXT["alt_annotation_month"], y=107,
            text=TXT["alt_annotation_text"],
            showarrow=False,
            font=dict(size=10, color=THEME["green"]),
        ),
    ],
)
st.plotly_chart(fig_alt, use_container_width=True, config={"displayModeBar": False})

render_html("alternance_banner.html", height=200, lang=LANG)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CONTACT + FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("<div id='contact' class='section-anchor'></div>", unsafe_allow_html=True)
render_html("contact.html", height=380, lang=LANG)
