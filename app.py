import base64
import os
from functools import lru_cache
from pathlib import Path

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from nicegui import app as nicegui_app, ui

ASSETS_DIR = Path(__file__).parent / "assets"
nicegui_app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")


@lru_cache(maxsize=10)
def _get_pdf_b64(filename: str) -> str:
    return base64.b64encode((ASSETS_DIR / filename).read_bytes()).decode()


# ── CSS ───────────────────────────────────────────────────────────────────────
# Place your background image at assets/bg.jpg (or change the URL below)
_CSS = """
:root {
    --bg:#050c14;
    --card:#081320;
    --text:#ffffff;
    --muted:rgba(255,255,255,0.55);
    --border:hsla(0,0%,100%,0.18);
    --accent:#7eb8d4;
    --green:#6ecf97;
    --amber:#e8c87a;
    --purple:#b89fe8;
}
*,*::before,*::after { box-sizing:border-box; margin:0; padding:0; }
html {
    scroll-behavior:smooth;
    scroll-padding-top:56px;
}
body {
    color:var(--text);
    background-color:var(--bg);
    font-family:'Source Sans 3','Source Sans Pro',sans-serif;
    font-weight:300;
    font-size:16px;
    line-height:1.75;
    -webkit-font-smoothing:antialiased;
}
a { color:inherit; text-decoration:none; }
.w { max-width:55em; margin:0 auto; padding:0 2rem; }

/* ── Navbar ─────────────────────────────────────────────────────── */
.nav {
    position:fixed; top:0; left:0; right:0; z-index:100;
    background:rgba(8,19,32,0.95);
    backdrop-filter:blur(8px); -webkit-backdrop-filter:blur(8px);
    border-bottom:1px solid var(--border);
    height:3.5em;
}
.nav-i {
    max-width:55em; margin:0 auto; padding:0 2rem;
    height:100%; display:flex; align-items:center; justify-content:space-between;
}
.nav-logo {
    font-family:'Raleway',sans-serif; font-weight:700;
    font-size:13px; letter-spacing:0.15em; text-transform:uppercase;
    color:var(--text);
}
.nav-links { display:flex; list-style:none; gap:0; }
.nav-links a {
    padding:0 0.9em; font-family:'Raleway',sans-serif;
    font-size:11px; font-weight:600; letter-spacing:0.12em; text-transform:uppercase;
    color:var(--muted); transition:color 0.2s;
}
.nav-links a:hover { color:var(--text); }
.nav-r { display:flex; align-items:center; gap:10px; }
.nav-lang {
    font-family:'Raleway',sans-serif;
    font-size:10px; font-weight:700; letter-spacing:0.12em; text-transform:uppercase;
    color:var(--muted); padding:5px 12px;
    border:1px solid var(--border);
    border-radius:3px; transition:all 0.2s;
}
.nav-lang:hover { color:var(--text); border-color:rgba(255,255,255,0.4); }
.theme-btn {
    width:30px; height:30px;
    display:flex; align-items:center; justify-content:center;
    background:transparent; border:1px solid var(--border);
    border-radius:3px; cursor:pointer; color:var(--muted);
    font-size:13px; transition:all 0.2s;
}
.theme-btn:hover { color:var(--text); border-color:rgba(255,255,255,0.4); }

/* ── Intro section ──────────────────────────────────────────────── */
.intro-sec {
    background:var(--bg);
    padding:8em 0 5em;
}
.badge {
    display:inline-flex; align-items:center; gap:8px;
    margin-bottom:2em;
    font-family:'Raleway',sans-serif; font-size:10px; font-weight:700;
    letter-spacing:0.15em; text-transform:uppercase;
    color:var(--text);
    border:1px solid var(--border);
    padding:6px 16px; border-radius:3px;
}
.pulse {
    width:6px; height:6px; border-radius:50%;
    background:var(--green); animation:pulse 2s infinite; flex-shrink:0;
}
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.25;} }
.h-name {
    font-family:'Raleway',sans-serif;
    font-size:clamp(2.4rem,7vw,4.5rem); font-weight:700;
    letter-spacing:0.06em; text-transform:uppercase;
    color:var(--text); line-height:1.1; margin-bottom:0.4em;
}
.h-role {
    font-family:'Raleway',sans-serif;
    font-size:clamp(1rem,2.5vw,1.3rem); font-weight:400;
    letter-spacing:0.2em; text-transform:uppercase;
    color:var(--muted); margin-bottom:1.6em;
    border-top:1px solid var(--border); padding-top:1em;
}
.h-desc {
    font-size:15px; color:var(--muted); font-weight:300;
    line-height:1.8; max-width:34em; margin-bottom:2.2em;
}
.btns { display:flex; gap:12px; flex-wrap:wrap; }
.btn {
    display:inline-flex; align-items:center; gap:6px;
    font-family:'Raleway',sans-serif; font-size:10.5px; font-weight:700;
    letter-spacing:0.12em; text-transform:uppercase;
    padding:0 2em; height:3em; border-radius:3px;
    border:1px solid var(--border); cursor:pointer;
    transition:all 0.2s; text-decoration:none;
}
.btn-p { background:rgba(255,255,255,0.08); color:var(--text); border-color:var(--border); }
.btn-p:hover { background:rgba(255,255,255,0.15); border-color:rgba(255,255,255,0.5); }
.btn-g { background:transparent; color:var(--muted); border-color:var(--border); }
.btn-g:hover { color:var(--text); border-color:rgba(255,255,255,0.4); }

/* ── Sections rectangulaires ────────────────────────────────────── */
.sec {
    background:var(--bg);
    padding:5em 0;
    border-top:1px solid var(--border);
}

/* ── Section text hierarchy ─────────────────────────────────────── */
.lbl {
    font-family:'Raleway',sans-serif;
    font-size:9.5px; letter-spacing:0.2em; text-transform:uppercase;
    color:var(--muted); margin-bottom:0.6em;
}
.ttl {
    font-family:'Raleway',sans-serif;
    font-size:clamp(1.5rem,3.5vw,2rem); font-weight:700;
    letter-spacing:0.06em; text-transform:uppercase;
    color:var(--text); margin-bottom:1.8em;
    padding-bottom:0.8em;
    border-bottom:1px solid var(--border);
}
.dsc { color:var(--muted); font-size:14px; font-weight:300; margin-bottom:1.8em; }

/* ── About ──────────────────────────────────────────────────────── */
.about-p { font-size:15px; color:var(--muted); font-weight:300; line-height:1.85; margin-bottom:1.8em; }
.about-p strong { color:var(--text); font-weight:600; }
.ftags { display:flex; gap:8px; flex-wrap:wrap; margin-top:0.5em; }
.ftag {
    display:inline-flex; align-items:center; gap:8px;
    padding:8px 16px; font-size:12px; font-weight:400;
    letter-spacing:0.06em; color:var(--muted);
    border:1px solid var(--border); border-radius:3px;
    background:var(--card);
}
.dot { width:5px; height:5px; border-radius:50%; flex-shrink:0; }
.db { background:var(--accent); }
.dp { background:var(--purple); }
.dg { background:var(--green); }

/* ── Skills ─────────────────────────────────────────────────────── */
.sg { display:flex; flex-direction:column; gap:1.8em; }
.sg-lbl {
    font-family:'Raleway',sans-serif; font-size:9.5px;
    text-transform:uppercase; letter-spacing:0.18em;
    color:var(--muted); margin-bottom:0.8em;
}
.tags { display:flex; flex-wrap:wrap; gap:8px; }
.tag {
    padding:6px 14px; font-size:12.5px; font-weight:300;
    border-radius:3px; border:1px solid var(--border);
    background:var(--card); color:var(--text);
}
.ta { border-color:rgba(126,184,212,0.3); color:var(--accent); background:rgba(126,184,212,0.06); }
.tg { border-color:rgba(110,207,151,0.3); color:var(--green); background:rgba(110,207,151,0.06); }
.tm { border-color:rgba(232,200,122,0.3); color:var(--amber); background:rgba(232,200,122,0.06); }
.tp { border-color:rgba(184,159,232,0.3); color:var(--purple); background:rgba(184,159,232,0.06); }

/* ── Experience ──────────────────────────────────────────────────── */
.elist { display:flex; flex-direction:column; gap:1em; }
.ec {
    padding:1.5em 1.8em;
    background:var(--card);
    border:1px solid var(--border);
    border-radius:3px;
    transition:border-color 0.25s;
}
.ec:hover { border-color:rgba(255,255,255,0.4); }
.ec-h {
    display:flex; justify-content:space-between; align-items:flex-start;
    flex-wrap:wrap; gap:8px; margin-bottom:0.7em;
}
.ec-t {
    font-family:'Raleway',sans-serif; font-size:13px; font-weight:700;
    letter-spacing:0.06em; text-transform:uppercase; color:var(--text);
}
.ec-c { font-size:13px; color:var(--muted); font-weight:300; margin-top:3px; }
.ec-r { text-align:right; }
.ec-d { font-size:11.5px; color:var(--muted); font-weight:300; letter-spacing:0.06em; }
.ongoing {
    display:inline-block; font-family:'Raleway',sans-serif;
    font-size:9px; font-weight:700;
    text-transform:uppercase; letter-spacing:0.12em; color:var(--green);
    border:1px solid rgba(110,207,151,0.35);
    border-radius:2px; padding:2px 8px; margin-top:4px;
}
.ec-desc { font-size:13.5px; color:var(--muted); font-weight:300; line-height:1.7; margin-bottom:0.7em; }
.ec-tags { font-size:11px; color:var(--muted); letter-spacing:0.06em; opacity:0.7; }

/* ── Projects ────────────────────────────────────────────────────── */
.pgrid { display:grid; grid-template-columns:1fr 1fr; gap:1em; }
.pc {
    padding:1.5em 1.8em;
    background:var(--card);
    border:1px solid var(--border);
    border-radius:3px;
    transition:border-color 0.25s, transform 0.2s;
    display:flex; flex-direction:column;
}
.pc:hover { border-color:rgba(255,255,255,0.4); transform:translateY(-2px); }
.pb {
    display:inline-block; font-family:'Raleway',sans-serif;
    font-size:9px; font-weight:700;
    text-transform:uppercase; letter-spacing:0.12em;
    padding:3px 10px; border-radius:2px; margin-bottom:0.9em;
}
.pb-etl { color:var(--green); border:1px solid rgba(110,207,151,0.35); }
.pb-ai  { color:var(--purple); border:1px solid rgba(184,159,232,0.35); }
.pb-mon { color:var(--amber); border:1px solid rgba(232,200,122,0.35); }
.pb-cli { color:var(--accent); border:1px solid rgba(126,184,212,0.35); }
.pt {
    font-family:'Raleway',sans-serif; font-size:13px; font-weight:700;
    letter-spacing:0.06em; text-transform:uppercase; color:var(--text); margin-bottom:0.6em;
}
.pd { font-size:13.5px; color:var(--muted); font-weight:300; line-height:1.7; flex:1; }
.ps { margin-top:1em; font-size:10.5px; color:var(--muted); letter-spacing:0.05em; opacity:0.6; }
.pl {
    display:inline-flex; align-items:center; gap:4px; margin-top:1em;
    font-family:'Raleway',sans-serif;
    font-size:10px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;
    color:var(--muted); transition:color 0.2s;
}
.pl:hover { color:var(--text); }

/* ── Apprenticeship callout ──────────────────────────────────────── */
.callout {
    padding:2em 2.2em;
    background:var(--card);
    border:1px solid var(--border);
    border-radius:3px;
}
.callout-t {
    font-family:'Raleway',sans-serif; font-size:15px; font-weight:700;
    letter-spacing:0.06em; text-transform:uppercase; color:var(--text); margin-bottom:0.5em;
}
.callout-s { font-size:14px; color:var(--muted); font-weight:300; line-height:1.75; }
.callout-s strong { color:var(--text); font-weight:600; }

/* ── CV ──────────────────────────────────────────────────────────── */
.cv-tb {
    display:flex; align-items:center; justify-content:space-between;
    flex-wrap:wrap; gap:10px; margin-bottom:1em;
}
.cv-tabs { display:flex; gap:6px; }
.cv-tab {
    padding:6px 18px; border-radius:3px;
    font-family:'Raleway',sans-serif;
    font-size:10px; font-weight:700; letter-spacing:0.12em; text-transform:uppercase;
    border:1px solid var(--border); color:var(--muted);
    background:transparent; cursor:pointer; transition:all 0.2s;
}
.cv-tab.active { background:rgba(255,255,255,0.1); color:var(--text); border-color:rgba(255,255,255,0.4); }
.cv-tab:hover:not(.active) { color:var(--text); border-color:rgba(255,255,255,0.35); }
.cv-acts { display:flex; gap:8px; flex-wrap:wrap; }
.cv-dl {
    display:inline-flex; align-items:center; gap:6px; padding:6px 18px;
    font-family:'Raleway',sans-serif;
    font-size:10px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;
    text-decoration:none; border-radius:3px; transition:all 0.2s;
}
.cv-dl-p { background:rgba(255,255,255,0.1); color:var(--text); border:1px solid rgba(255,255,255,0.35); }
.cv-dl-p:hover { background:rgba(255,255,255,0.18); }
.cv-dl-s { background:transparent; color:var(--muted); border:1px solid var(--border); }
.cv-dl-s:hover { color:var(--text); border-color:rgba(255,255,255,0.35); }
.cv-view {
    border:1px solid var(--border); border-radius:3px;
    height:600px; background:#525659; overflow-y:auto; padding:10px;
}
.cv-load {
    display:flex; align-items:center; justify-content:center;
    height:100%; color:var(--muted); font-size:13px; gap:8px;
}
.cv-spin {
    width:16px; height:16px; border-radius:50%;
    border:2px solid rgba(255,255,255,0.15);
    border-top-color:var(--accent); animation:spin 0.8s linear infinite;
}
@keyframes spin { to { transform:rotate(360deg); } }
.pdf-pages canvas { width:100%; display:block; margin-bottom:6px; box-shadow:0 2px 10px rgba(0,0,0,0.4); }
.cv-hidden { display:none !important; }

/* ── Contact ─────────────────────────────────────────────────────── */
.cgrid { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:1.5em; }
.cc {
    display:flex; align-items:center; gap:14px; padding:1em 1.4em;
    background:var(--card); border:1px solid var(--border);
    border-radius:3px; color:var(--muted); font-size:13px;
    font-weight:300; transition:all 0.2s;
}
.cc:hover { color:var(--text); border-color:rgba(255,255,255,0.4); }
.ci {
    width:34px; height:34px; display:flex; align-items:center; justify-content:center;
    border:1px solid var(--border); border-radius:3px; font-size:15px; flex-shrink:0;
    background:rgba(255,255,255,0.04);
}
.footer {
    padding:2em; text-align:center;
    background:transparent;
    font-family:'Raleway',sans-serif; font-size:9.5px; letter-spacing:0.15em;
    text-transform:uppercase; color:var(--muted);
}

/* ── Responsive ──────────────────────────────────────────────────── */
@media (max-width:640px) {
    .nav-links { display:none; }
    .h-name { font-size:2rem; }
    .pgrid { grid-template-columns:1fr; }
    .cgrid { grid-template-columns:1fr; }
    .cv-tb { flex-direction:column; align-items:flex-start; }
    .sec { padding:3em 0; }
    .intro-sec { padding:6em 0 3em; }
    .ec-h { flex-direction:column; gap:4px; }
    .ec-r { text-align:left; }
    .btns { gap:8px; }
    .btn { height:2.8em; font-size:10px; }
}
"""

_JS_TEMPLATE = r"""
pdfjsLib.GlobalWorkerOptions.workerSrc='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
var PDF_P='__PDF_P__',PDF_S='__PDF_S__';
var ldP=false,ldS=false;
function b2b(b){var r=atob(b),a=new Uint8Array(r.length);for(var i=0;i<r.length;i++)a[i]=r.charCodeAt(i);return a;}
function rPDF(b,pid,lel){
  var c=document.getElementById(pid);
  pdfjsLib.getDocument({data:b2b(b)}).promise.then(function(pdf){
    if(lel)lel.style.display='none';
    for(var p=1;p<=pdf.numPages;p++){(function(n){
      var ph=document.createElement('div');c.appendChild(ph);
      pdf.getPage(n).then(function(pg){
        var w=c.offsetWidth||800,nat=pg.getViewport({scale:1}),vp=pg.getViewport({scale:w/nat.width});
        var cv=document.createElement('canvas');cv.width=vp.width;cv.height=vp.height;
        ph.appendChild(cv);pg.render({canvasContext:cv.getContext('2d'),viewport:vp});
      });
    })(p);}
  }).catch(function(e){if(lel)lel.innerHTML='';c.innerHTML='<p style="color:#f87171;padding:16px">Error: '+e.message+'</p>';});
}
document.getElementById('__DP_ID__').href='data:application/pdf;base64,'+PDF_P;
document.getElementById('__DS_ID__').href='data:application/pdf;base64,'+PDF_S;
var lel=document.querySelector('#__VP_ID__ .cv-load');
rPDF(PDF_P,'__PP_ID__',lel);ldP=true;
function showCV(l){
  var ip=l==='__LP__';
  document.getElementById('__VP_ID__').classList.toggle('cv-hidden',!ip);
  document.getElementById('__VS_ID__').classList.toggle('cv-hidden',ip);
  document.getElementById('__TP_ID__').classList.toggle('active',ip);
  document.getElementById('__TS_ID__').classList.toggle('active',!ip);
  if(!ldS&&!ip){rPDF(PDF_S,'__PS_ID__',null);ldS=true;}
}
function toggleTheme(){
  var t=document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark';
  document.documentElement.setAttribute('data-theme',t);localStorage.setItem('theme',t);
  var b=document.getElementById('tbtn');if(b)b.textContent=t==='dark'?'◑':'◐';
}
document.addEventListener('DOMContentLoaded',function(){
  var b=document.getElementById('tbtn');
  if(b){var t=localStorage.getItem('theme')||'dark';b.textContent=t==='dark'?'◑':'◐';}
});
"""


def _build_page(lang: str) -> str:
    fr = lang == "FR"
    pdf_fr = _get_pdf_b64("CV_FR_PRINCIPAL.pdf")
    pdf_en = _get_pdf_b64("CV_Ibrahim_Kara_en.pdf")
    pdf_p  = pdf_fr if fr else pdf_en
    pdf_s  = pdf_en if fr else pdf_fr

    # CV element IDs
    vp_id = "viewer-fr" if fr else "viewer-en"
    vs_id = "viewer-en" if fr else "viewer-fr"
    pp_id = "pages-fr"  if fr else "pages-en"
    ps_id = "pages-en"  if fr else "pages-fr"
    tp_id = "tab-fr"    if fr else "tab-en"
    ts_id = "tab-en"    if fr else "tab-fr"
    dp_id = "dl-fr"     if fr else "dl-en"
    ds_id = "dl-en"     if fr else "dl-fr"
    lp    = "fr"        if fr else "en"
    ls    = "en"        if fr else "fr"   # noqa: F841

    tab_p_lbl = "Français" if fr else "English"
    tab_s_lbl = "English"  if fr else "Français"
    dl_p_lbl  = "Télécharger CV FR" if fr else "Download CV EN"
    dl_s_lbl  = "Download CV EN"    if fr else "Télécharger CV FR"
    dl_p_name = "CV_Ibrahim_Kara_FR.pdf" if fr else "CV_Ibrahim_Kara_en.pdf"
    dl_s_name = "CV_Ibrahim_Kara_en.pdf" if fr else "CV_Ibrahim_Kara_FR.pdf"
    cv_loading = "Chargement…" if fr else "Loading…"
    cv_sub     = "Disponible en français et en anglais" if fr else "Available in French and English"

    js = (_JS_TEMPLATE
          .replace("__PDF_P__", pdf_p).replace("__PDF_S__", pdf_s)
          .replace("__VP_ID__", vp_id).replace("__VS_ID__", vs_id)
          .replace("__PP_ID__", pp_id).replace("__PS_ID__", ps_id)
          .replace("__TP_ID__", tp_id).replace("__TS_ID__", ts_id)
          .replace("__DP_ID__", dp_id).replace("__DS_ID__", ds_id)
          .replace("__LP__",    lp))

    lang_href = "/?lang=en" if fr else "/?lang=fr"
    lang_lbl  = "EN"        if fr else "FR"

    # ── Hero ──────────────────────────────────────────────────────────────────
    avail  = "Disponible en alternance · Sept 2026" if fr else "Open for Apprenticeship · Sep 2026"
    h_desc = (
        "Étudiant à l'Efrei Paris, je passe du développement web à la Data Engineering & IA. "
        "Je cherche une alternance de 24 mois à partir de septembre 2026."
    ) if fr else (
        "Efrei Paris student transitioning from web development to Data Engineering & AI. "
        "Looking for a 24-month apprenticeship starting September 2026."
    )
    cta_proj    = "Voir mes projets" if fr else "See my projects"
    cta_contact = "Me contacter"     if fr else "Get in touch"

    # ── About ─────────────────────────────────────────────────────────────────
    about_lbl  = "À propos"       if fr else "About"
    about_ttl  = "Qui suis-je ?"  if fr else "Who I am"
    about_text = (
        "Actuellement en 3ème année à l'Efrei Paris (Licence Web → Mastère Data Engineering & IA, 2023–2028), "
        "j'ai appris à construire des applications web fullstack — des bases que j'applique désormais à des problématiques data. "
        "Mon focus se porte sur la <strong>structuration et la transformation de données</strong>, "
        "ainsi que sur l'intégration de <strong>LLMs</strong> dans des produits réels."
    ) if fr else (
        "Currently in my 3rd year at Efrei Paris (Web Bachelor's → Data &amp; AI Master's, 2023–2028), "
        "I've built full-stack web applications — a foundation I now apply to data challenges. "
        "My focus is on <strong>structuring and transforming data</strong> "
        "and integrating <strong>LLMs</strong> into real products."
    )
    focus3 = "Mastère Data & IA · Efrei Paris" if fr else "Data &amp; AI Master's · Efrei Paris"

    # ── Skills ────────────────────────────────────────────────────────────────
    sk_lbl  = "Compétences" if fr else "Skills"
    sk_ttl  = "Mon stack"   if fr else "My stack"
    sk_lang = "Langages"    if fr else "Languages"
    sk_data = "Data & IA"   if fr else "Data & AI"

    # ── Experience ────────────────────────────────────────────────────────────
    exp_lbl     = "Parcours"    if fr else "Journey"
    exp_ttl     = "Expériences" if fr else "Experience"
    exp_ongoing = "En cours"    if fr else "Ongoing"

    e1t = "Développeur R&D — Stagiaire" if fr else "R&D Developer — Intern"
    e1c = "Study'UP · Argenteuil"
    e1d = "Fév–Mai 2026" if fr else "Feb–May 2026"
    e1x = (
        "Intégration d'un LLM (Anthropic) via Python pour des explications adaptées "
        "de l'école primaire au lycée. Interface Next.js avec streaming LLM. "
        "Prompt engineering avec approche socratique."
    ) if fr else (
        "Integrated an LLM (Anthropic) via Python to generate adaptive explanations "
        "from primary to high school. Next.js chat interface with LLM streaming. "
        "Prompt engineering with a Socratic approach."
    )
    e1s = "Next.js · Python · LLM · Prompt Engineering"

    e2t = "Développeur Web — Stagiaire" if fr else "Web Developer — Intern"
    e2c = "France Patrimoine Emc · Le Plessis-Trévise"
    e2d = "Juin–Juil 2025" if fr else "Jun–Jul 2025"
    e2x = (
        "Application interne Vue.js pour le suivi commercial : gestion des leads, "
        "rendez-vous, dossiers et signatures. Espace admin pour la supervision des performances."
    ) if fr else (
        "Internal Vue.js app for sales tracking: lead management, meetings, files, signatures. "
        "Admin area for user management and performance supervision."
    )
    e2s = "Vue.js · JavaScript"

    e3t = "Développeur Web — Stagiaire" if fr else "Web Developer — Intern"
    e3c = "Alexis Finance · Noisy-le-Grand"
    e3d = "Mai–Juil 2024" if fr else "May–Jul 2024"
    e3x = (
        "Optimisation UX du site web en collaboration avec l'équipe. "
        "Création et intégration de vidéos de formation."
    ) if fr else (
        "Website UX optimization in collaboration with the team. "
        "Creation and integration of training videos."
    )
    e3s = "JavaScript · UX"

    # ── Projects ──────────────────────────────────────────────────────────────
    pr_lbl  = "Travaux"  if fr else "Work"
    pr_ttl  = "Projets"  if fr else "Projects"

    p1d = (
        "Pipeline ETL en Python pour traiter et nettoyer des logs serveurs simulés, "
        "avec stockage structuré dans PostgreSQL."
    ) if fr else (
        "Python ETL pipeline to process and clean simulated server logs "
        "with structured storage in PostgreSQL."
    )
    p2d = (
        "Outil d'analyse de documents utilisant un LLM pour des résumés "
        "automatisés et l'extraction de points clés."
    ) if fr else (
        "Document analysis tool using an LLM for automated summaries "
        "and key insight extraction."
    )
    p3d = (
        "Interface de monitoring CPU/RAM avec métriques simulées, "
        "stockées en SQL et visualisées avec Plotly."
    ) if fr else (
        "CPU/RAM monitoring interface with simulated metrics "
        "stored in SQL and visualized through Plotly."
    )
    p4d = (
        "Site pro pour une entreprise de rénovation énergétique en Île-de-France. "
        "Formulaire de contact avec email + devis PDF auto, galerie Supabase, CI/CD Vercel."
    ) if fr else (
        "Professional site for an energy renovation company in Île-de-France. "
        "Contact form with email + auto PDF quote, Supabase gallery, Vercel CI/CD."
    )
    p4badge = "Client"   if fr else "Client Work"
    p2badge = "IA"       if fr else "AI"

    # ── Alternance ────────────────────────────────────────────────────────────
    alt_lbl  = "Opportunité"        if fr else "Opportunity"
    alt_ttl  = "Alternance 24 mois" if fr else "24-Month Apprenticeship"
    alt_head = "Disponible en alternance · Septembre 2026" if fr else "Open for Apprenticeship · September 2026"
    alt_sub  = "Mastère Data Engineering & IA · Efrei Paris" if fr else "Data Engineering &amp; AI Master's · Efrei Paris"
    alt_body = (
        "Je recherche une <strong>alternance de 24 mois</strong> dans l'un de ces deux domaines :<br><br>"
        "→ <strong>Développement Full Stack &amp; IA</strong><br>"
        "→ <strong>Data Engineering &amp; IA</strong><br><br>"
        "Motivé, curieux et à l'aise aussi bien côté front que back, je cherche à contribuer à des projets concrets "
        "tout en continuant à progresser."
    ) if fr else (
        "I am looking for a <strong>24-month work-study contract</strong> in one of these two fields:<br><br>"
        "→ <strong>Full Stack Development &amp; AI</strong><br>"
        "→ <strong>Data Engineering &amp; AI</strong><br><br>"
        "Motivated and comfortable on both front-end and back-end, I want to contribute to real projects "
        "while continuing to grow."
    )
    alt_rhy = "Rythme : pas encore communiqué par l'école" if fr else "Schedule: not yet communicated by the school"

    # ── Contact ───────────────────────────────────────────────────────────────
    ct_lbl  = "Disponible · Sept 2026" if fr else "Available · Sep 2026"
    ct_back = "Retour en haut"         if fr else "Back to top"
    footer  = (
        "Ibrahim Karamanlian · 2026 · Efrei Paris · Bac +3 Data & IA"
    ) if fr else (
        "Ibrahim Karamanlian · 2026 · Efrei Paris · Year 3 Data & AI"
    )

    # ── Nav labels ────────────────────────────────────────────────────────────
    nav_about = "À propos"   if fr else "About"
    nav_exp   = "Expérience" if fr else "Experience"
    nav_proj  = "Projets"    if fr else "Projects"

    # ── HTML ──────────────────────────────────────────────────────────────────
    head = (
        f'<!DOCTYPE html>\n<html lang="{lang.lower()}" data-theme="dark">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>Ibrahim Karamanlian | Data Engineer</title>\n'
        '<script>!function(){var t=localStorage.getItem("theme")||"dark";'
        'document.documentElement.setAttribute("data-theme",t);}();</script>\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link href="https://fonts.googleapis.com/css2?'
        'family=Raleway:wght@300;400;600;700;800'
        '&family=Source+Sans+3:wght@300;400;600'
        '&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">\n'
        '<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32x32.png">\n'
        '<link rel="manifest" href="/assets/manifest.json">\n'
        f'<style>{_CSS}</style>\n'
        '</head>\n<body>\n'
    )

    navbar = (
        '<nav class="nav">\n'
        '  <div class="nav-i">\n'
        '    <div class="nav-logo">Ibrahim<span>.</span></div>\n'
        '    <ul class="nav-links">\n'
        f'      <li><a href="#about">{nav_about}</a></li>\n'
        '      <li><a href="#skills">Stack</a></li>\n'
        f'      <li><a href="#experience">{nav_exp}</a></li>\n'
        f'      <li><a href="#projects">{nav_proj}</a></li>\n'
        '      <li><a href="#cv">CV</a></li>\n'
        '      <li><a href="#contact">Contact</a></li>\n'
        '    </ul>\n'
        '    <div class="nav-r">\n'
        f'      <a href="{lang_href}" class="nav-lang">{lang_lbl}</a>\n'
        '      <button class="theme-btn" id="tbtn" onclick="toggleTheme()">◑</button>\n'
        '    </div>\n'
        '  </div>\n'
        '</nav>\n'
    )


    # Intro — première section opaque avec nom / rôle / CTAs
    intro = (
        '<section id="intro" class="intro-sec">\n'
        '  <div class="w">\n'
        f'    <div class="badge"><span class="pulse"></span>{avail}</div>\n'
        '    <h1 class="h-name">Ibrahim Karamanlian</h1>\n'
        '    <div class="h-role">Data Engineer</div>\n'
        f'    <p class="h-desc">{h_desc}</p>\n'
        '    <div class="btns">\n'
        f'      <a href="#projects" class="btn btn-p">{cta_proj}</a>\n'
        f'      <a href="#contact" class="btn btn-g">{cta_contact}</a>\n'
        f'      <a href="data:application/pdf;base64,{pdf_p}" download="{dl_p_name}" class="btn btn-g">↓ CV</a>\n'
        '    </div>\n'
        '  </div>\n'
        '</section>\n'
    )

    # Helper: section block with diagonal fill
    def sec(anchor, content):
        return (
            f'<section id="{anchor}" class="sec">\n'
            '  <div class="w">\n'
            + content +
            '  </div>\n'
            '</section>\n'
        )

    about_content = (
        f'    <div class="lbl">{about_lbl}</div>\n'
        f'    <h2 class="ttl">{about_ttl}</h2>\n'
        f'    <p class="about-p">{about_text}</p>\n'
        '    <div class="ftags">\n'
        '      <span class="ftag"><span class="dot db"></span>Data Engineering</span>\n'
        '      <span class="ftag"><span class="dot dp"></span>LLMs &amp; IA générative</span>\n'
        f'      <span class="ftag"><span class="dot dg"></span>{focus3}</span>\n'
        '    </div>\n'
    )

    skills_content = (
        f'    <div class="lbl">{sk_lbl}</div>\n'
        f'    <h2 class="ttl">{sk_ttl}</h2>\n'
        '    <div class="sg">\n'
        f'      <div><div class="sg-lbl">{sk_lang}</div><div class="tags">'
        '<span class="tag ta">Python</span>'
        '<span class="tag ta">JavaScript</span>'
        '<span class="tag ta">TypeScript</span>'
        '<span class="tag ta">SQL</span>'
        '<span class="tag ta">PHP</span>'
        '<span class="tag ta">HTML / CSS</span>'
        '</div></div>\n'
        '      <div><div class="sg-lbl">Frameworks &amp; Libs</div><div class="tags">'
        '<span class="tag tg">React</span>'
        '<span class="tag tg">Next.js</span>'
        '<span class="tag tg">Vue.js</span>'
        '<span class="tag tg">Node.js</span>'
        '<span class="tag tg">Express.js</span>'
        '<span class="tag tg">FastAPI</span>'
        '<span class="tag tg">Tailwind CSS</span>'
        '<span class="tag tg">Symfony</span>'
        '</div></div>\n'
        '      <div><div class="sg-lbl">Infra &amp; Outils</div><div class="tags">'
        '<span class="tag tm">Docker</span>'
        '<span class="tag tm">PostgreSQL</span>'
        '<span class="tag tm">MySQL</span>'
        '<span class="tag tm">MongoDB</span>'
        '<span class="tag tm">Supabase</span>'
        '<span class="tag tm">Git / GitHub</span>'
        '<span class="tag tm">GitHub Actions</span>'
        '<span class="tag tm">REST API</span>'
        '<span class="tag tm">Postman</span>'
        '</div></div>\n'
        f'      <div><div class="sg-lbl">{sk_data}</div><div class="tags">'
        '<span class="tag tp">ETL / Pipelines</span>'
                '<span class="tag tp">LLMs</span>'
        '<span class="tag tp">Prompt Engineering</span>'
        '</div></div>\n'
        '    </div>\n'
    )

    exp_content = (
        f'    <div class="lbl">{exp_lbl}</div>\n'
        f'    <h2 class="ttl">{exp_ttl}</h2>\n'
        '    <div class="elist">\n'
        '      <div class="ec">\n'
        '        <div class="ec-h">\n'
        f'          <div><div class="ec-t">{e1t}</div><div class="ec-c">{e1c}</div></div>\n'
        f'          <div class="ec-r"><div class="ec-d">{e1d}</div><div class="ongoing">{exp_ongoing}</div></div>\n'
        '        </div>\n'
        f'        <div class="ec-desc">{e1x}</div>\n'
        f'        <div class="ec-tags">{e1s}</div>\n'
        '      </div>\n'
        '      <div class="ec">\n'
        '        <div class="ec-h">\n'
        f'          <div><div class="ec-t">{e2t}</div><div class="ec-c">{e2c}</div></div>\n'
        f'          <div class="ec-r"><div class="ec-d">{e2d}</div></div>\n'
        '        </div>\n'
        f'        <div class="ec-desc">{e2x}</div>\n'
        f'        <div class="ec-tags">{e2s}</div>\n'
        '      </div>\n'
        '      <div class="ec">\n'
        '        <div class="ec-h">\n'
        f'          <div><div class="ec-t">{e3t}</div><div class="ec-c">{e3c}</div></div>\n'
        f'          <div class="ec-r"><div class="ec-d">{e3d}</div></div>\n'
        '        </div>\n'
        f'        <div class="ec-desc">{e3x}</div>\n'
        f'        <div class="ec-tags">{e3s}</div>\n'
        '      </div>\n'
        '    </div>\n'
    )

    proj_content = (
        f'    <div class="lbl">{pr_lbl}</div>\n'
        f'    <h2 class="ttl">{pr_ttl}</h2>\n'
        '    <div class="pgrid">\n'
        '      <div class="pc">\n'
        '        <span class="pb pb-etl">Pipeline ETL</span>\n'
        '        <div class="pt">Log-Processing-Pipeline</div>\n'
        f'        <div class="pd">{p1d}</div>\n'
        '        <div class="ps">Python · Pandas · PostgreSQL · Docker</div>\n'
        '        <div style="margin-top:8px;font-size:10.5px;color:var(--muted);opacity:0.55;letter-spacing:0.04em;">réalisé avec Claude</div>\n'
        '        <a href="https://github.com/Kibraa/LogStream-Architect" target="_blank" class="pl">↗ GitHub</a>\n'
        '      </div>\n'
        '      <div class="pc">\n'
        f'        <span class="pb pb-ai">{p2badge}</span>\n'
        '        <div class="pt">Text-Analyzer</div>\n'
        f'        <div class="pd">{p2d}</div>\n'
        '        <div class="ps">Python · LLM API</div>\n'
        '        <div style="margin-top:8px;font-size:10.5px;color:var(--muted);opacity:0.55;letter-spacing:0.04em;">réalisé avec Claude</div>\n'
        '        <a href="https://github.com/Kibraa/semantic-brain" target="_blank" class="pl">↗ GitHub</a>\n'
        '      </div>\n'
        '      <div class="pc">\n'
        '        <span class="pb pb-mon">Monitoring</span>\n'
        '        <div class="pt">Metric-Board</div>\n'
        f'        <div class="pd">{p3d}</div>\n'
        '        <div class="ps">Next.js · SQL · Plotly · Tailwind</div>\n'
        '        <div style="margin-top:8px;font-size:10.5px;color:var(--muted);opacity:0.55;letter-spacing:0.04em;">réalisé avec Claude</div>\n'
        '        <a href="https://github.com/Kibraa/Metric-Board" target="_blank" class="pl">↗ GitHub</a>\n'
        '      </div>\n'
        '      <div class="pc">\n'
        f'        <span class="pb pb-cli">{p4badge}</span>\n'
        '        <div class="pt">3MECO</div>\n'
        f'        <div class="pd">{p4d}</div>\n'
        '        <div class="ps">Vue 3 · Node.js · Supabase · Vercel</div>\n'
        '        <a href="https://3-m-eco.vercel.app" target="_blank" class="pl">↗ Voir le site</a>\n'
        '      </div>\n'
        '    </div>\n'
    )

    alt_content = (
        f'    <div class="lbl">{alt_lbl}</div>\n'
        f'    <h2 class="ttl">{alt_ttl}</h2>\n'
        '    <div class="callout">\n'
        f'      <div class="callout-t">{alt_head}</div>\n'
        f'      <div class="callout-s" style="margin-top:6px;font-size:12px;color:var(--muted);opacity:0.7;">{alt_sub}</div>\n'
        f'      <div class="callout-s" style="margin-top:10px;">{alt_body}</div>\n'
        f'      <div class="callout-s" style="margin-top:14px;font-size:12px;opacity:0.5;">{alt_rhy}</div>\n'
        '    </div>\n'
    )

    cv_tab_onclick_p = f"showCV('{lp}')"
    cv_tab_onclick_s = f"showCV('{ls}')"
    cv_content = (
        '    <div class="lbl">CV</div>\n'
        f'    <h2 class="ttl">{"Mon CV" if fr else "My Resume"}</h2>\n'
        f'    <p class="dsc">{cv_sub}</p>\n'
        '    <div class="cv-tb">\n'
        '      <div class="cv-tabs">\n'
        f'        <button class="cv-tab active" id="{tp_id}" onclick="{cv_tab_onclick_p}" type="button">{tab_p_lbl}</button>\n'
        f'        <button class="cv-tab" id="{ts_id}" onclick="{cv_tab_onclick_s}" type="button">{tab_s_lbl}</button>\n'
        '      </div>\n'
        '      <div class="cv-acts">\n'
        f'        <a id="{dp_id}" class="cv-dl cv-dl-p" href="#" download="{dl_p_name}">{dl_p_lbl}</a>\n'
        f'        <a id="{ds_id}" class="cv-dl cv-dl-s" href="#" download="{dl_s_name}">{dl_s_lbl}</a>\n'
        '      </div>\n'
        '    </div>\n'
        '    <div class="cv-view">\n'
        f'      <div id="{vp_id}">\n'
        f'        <div class="cv-load"><div class="cv-spin"></div>{cv_loading}</div>\n'
        f'        <div class="pdf-pages" id="{pp_id}"></div>\n'
        '      </div>\n'
        f'      <div id="{vs_id}" class="cv-hidden">\n'
        f'        <div class="pdf-pages" id="{ps_id}"></div>\n'
        '      </div>\n'
        '    </div>\n'
    )

    contact_content = (
        f'    <div class="lbl">{ct_lbl}</div>\n'
        '    <h2 class="ttl">Contact</h2>\n'
        '    <div class="cgrid">\n'
        '      <a href="mailto:karamanlian.ibrahim@gmail.com" class="cc">\n'
        '        <div class="ci">📧</div>karamanlian.ibrahim@gmail.com\n'
        '      </a>\n'
        '      <a href="tel:+33646864447" class="cc">\n'
        '        <div class="ci">📱</div>06 46 86 44 47\n'
        '      </a>\n'
        '      <a href="https://github.com/Kibraa" target="_blank" class="cc">\n'
        '        <div class="ci">'
        '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">'
        '<path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387'
        '.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416'
        '-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729'
        ' 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997'
        '.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931'
        ' 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0'
        ' 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138'
        ' 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176'
        '.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921'
        '.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576'
        'C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/></svg>'
        '</div>github.com/Kibraa\n'
        '      </a>\n'
        '    </div>\n'
        f'    <div style="margin-top:40px;text-align:center;">'
        f'<button type="button" class="btn btn-g" '
        f'onclick="window.scrollTo({{top:0,behavior:\'smooth\'}})">↑ {ct_back}</button>'
        f'</div>\n'
    )

    scripts = (
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>\n'
        f'<script>{js}</script>\n'
    )

    return (
        head + navbar + intro
        + sec("about",      about_content)
        + sec("skills",     skills_content)
        + sec("experience", exp_content)
        + sec("projects",   proj_content)
        + sec("alternance", alt_content)
        + sec("cv",         cv_content)
        + sec("contact",    contact_content)
        + f'<div class="footer">{footer}</div>\n'
        + scripts
        + '</body>\n</html>'
    )


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
    reload=True,
    show=False,
)
