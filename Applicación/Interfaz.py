"""Components visuals reutilitzables per a la interfície Streamlit."""

from __future__ import annotations

import streamlit as st

# ---------------------------------------------------------------------------
# Estils
# ---------------------------------------------------------------------------

CSS = """
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --navy: #0B1F3A;
    --navy-2: #123459;
    --gold: #D9A441;
    --gold-soft: #F3E3BE;
    --red: #B3122E;
    --cream: #F6F2EA;
    --ink: #1C2430;
    --muted: #5D6B7A;
    --line: #E4DCCD;
    --green: #2F7D5C;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--ink);
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(1200px 600px at 85% -10%, rgba(217,164,65,0.10), transparent 60%),
        radial-gradient(900px 500px at -10% 20%, rgba(11,31,58,0.05), transparent 60%),
        var(--cream);
}

[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1240px;
}

h1, h2, h3, h4 {
    font-family: 'DM Serif Display', Georgia, serif;
    color: var(--navy);
    letter-spacing: -0.01em;
    font-weight: 400;
}

h1 { font-size: 2.35rem; line-height: 1.1; }
h2 { font-size: 1.65rem; }
h3 { font-size: 1.25rem; }

p, li, label, span, div { font-size: 0.98rem; }

/* ---------------- Sidebar ---------------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A1B33 0%, #0E2A4A 70%, #123459 100%);
    border-right: 1px solid rgba(217,164,65,0.25);
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #F3EEE5;
}
[data-testid="stSidebar"] .stRadio label p { color: #DCE4EE !important; font-weight: 500; }
[data-testid="stSidebar"] .stRadio [role="radiogroup"] { gap: 0.15rem; }
[data-testid="stSidebar"] .stRadio label:hover p { color: #FFFFFF !important; }
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
    padding: 0.38rem 0.65rem;
    border-radius: 9px;
    transition: background 0.15s ease;
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label:has(input:checked) {
    background: rgba(217,164,65,0.16);
    box-shadow: inset 3px 0 0 #D9A441;
}
[data-testid="stSidebar"] .stRadio [role="radiogroup"] label > div:first-child {
    display: none;
}
[data-testid="stSidebar"] .stButton > button {
    background: rgba(217,164,65,0.14);
    border: 1px solid rgba(217,164,65,0.55);
    color: #F6E7C4;
    font-weight: 600;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(217,164,65,0.26);
    border-color: #D9A441;
    color: #FFFFFF;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #D9A441, #B9822B);
    border: 1px solid #D9A441;
    color: #0B1F3A;
    box-shadow: 0 8px 20px rgba(0,0,0,0.25);
}
[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #E4B45A, #C68F31);
    color: #0B1F3A;
}
[data-testid="stSidebar"] .stButton > button p { color: inherit !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12); }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] a { color: var(--gold); }

.brand {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.4rem 0 0.9rem 0;
}
.brand-star {
    width: 40px; height: 40px; border-radius: 12px;
    background: linear-gradient(135deg, var(--gold), #B9822B);
    color: #0B1F3A; display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem; font-weight: 700;
    box-shadow: 0 6px 18px rgba(217,164,65,0.35);
}
.brand-name {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 1.35rem; color: #FFFFFF; line-height: 1;
}
.brand-sub {
    font-size: 0.72rem; letter-spacing: 0.14em; text-transform: uppercase;
    color: #9FB2C8; margin-top: 0.18rem;
}

/* ---------------- Hero ---------------- */
.hero {
    position: relative;
    background: linear-gradient(120deg, #0B1F3A 0%, #123459 58%, #1B4470 100%);
    border-radius: 22px;
    padding: 2.1rem 2.3rem 2rem 2.3rem;
    color: #F6F2EA;
    overflow: hidden;
    box-shadow: 0 18px 50px rgba(11,31,58,0.22);
    margin-bottom: 1.4rem;
}
.hero::after {
    content: "";
    position: absolute; right: -70px; top: -90px;
    width: 320px; height: 320px; border-radius: 50%;
    background: radial-gradient(circle, rgba(217,164,65,0.30), rgba(217,164,65,0) 70%);
}
.hero::before {
    content: "";
    position: absolute; right: 60px; bottom: -60px;
    width: 180px; height: 180px; border-radius: 50%;
    border: 1px solid rgba(217,164,65,0.35);
}
.hero-kicker {
    font-size: 0.72rem; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--gold); font-weight: 600; margin-bottom: 0.55rem;
}
.hero-title {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 2.35rem; line-height: 1.08; color: #FFFFFF;
    max-width: 780px; margin-bottom: 0.6rem;
}
.hero-title em { color: var(--gold); font-style: italic; }
.hero-text {
    color: #C9D6E4; max-width: 720px; font-size: 1.02rem; line-height: 1.55;
    margin-bottom: 0.1rem;
}
.hero-badges { margin-top: 1.05rem; display: flex; flex-wrap: wrap; gap: 0.45rem; }
.hero-badge {
    border: 1px solid rgba(217,164,65,0.45);
    background: rgba(217,164,65,0.10);
    color: #F0D9A6; border-radius: 999px;
    padding: 0.28rem 0.72rem; font-size: 0.76rem; letter-spacing: 0.02em;
}

/* ---------------- Mètriques ---------------- */
.metric {
    background: #FFFFFF;
    border: 1px solid var(--line);
    border-radius: 16px;
    padding: 1rem 1.1rem 0.95rem 1.1rem;
    height: 100%;
    box-shadow: 0 6px 18px rgba(28,36,48,0.04);
    position: relative;
    overflow: hidden;
}
.metric::before {
    content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 4px;
    background: linear-gradient(180deg, var(--gold), #B9822B);
}
.metric-value {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 1.95rem; color: var(--navy); line-height: 1.05;
}
.metric-label {
    font-size: 0.73rem; text-transform: uppercase; letter-spacing: 0.10em;
    color: var(--muted); font-weight: 600; margin-top: 0.35rem;
}
.metric-detail { font-size: 0.80rem; color: var(--muted); margin-top: 0.3rem; }

/* ---------------- Seccions ---------------- */
.section-kicker {
    font-size: 0.70rem; letter-spacing: 0.16em; text-transform: uppercase;
    color: var(--gold); font-weight: 700; margin-bottom: 0.25rem;
}
.section-title {
    font-family: 'DM Serif Display', Georgia, serif;
    font-size: 1.6rem; color: var(--navy); margin-bottom: 0.2rem;
}
.section-sub { color: var(--muted); font-size: 0.95rem; margin-bottom: 1rem; }

.pill {
    display: inline-block; padding: 0.18rem 0.6rem; border-radius: 999px;
    font-size: 0.72rem; font-weight: 600; letter-spacing: 0.02em;
    border: 1px solid transparent; white-space: nowrap;
}
.pill-gold { background: var(--gold-soft); color: #7A5410; border-color: #E8CD93; }
.pill-green { background: #DFF0E7; color: #1F6046; border-color: #B9DCCB; }
.pill-red { background: #F7DDE1; color: #8E1026; border-color: #EBB9C2; }
.pill-blue { background: #DDE8F4; color: #163C63; border-color: #BBD0E6; }
.pill-grey { background: #ECEAE4; color: #55606D; border-color: #DAD5C9; }

/* ---------------- Cicle ---------------- */
.cycle {
    display: grid; grid-template-columns: repeat(8, minmax(0, 1fr));
    gap: 0.4rem; margin: 0.4rem 0 0.6rem 0;
}
.cycle-step {
    background: #FFFFFF; border: 1px solid var(--line); border-radius: 12px;
    padding: 0.6rem 0.5rem; text-align: center; min-height: 78px;
}
.cycle-num {
    width: 22px; height: 22px; border-radius: 50%; margin: 0 auto 0.35rem auto;
    background: var(--navy); color: #fff; font-size: 0.7rem; font-weight: 700;
    display: flex; align-items: center; justify-content: center;
}
.cycle-label { font-size: 0.68rem; line-height: 1.2; color: var(--navy); font-weight: 600; }
@media (max-width: 900px) { .cycle { grid-template-columns: repeat(4, 1fr); } }

/* ---------------- Callouts ---------------- */
.callout {
    border-radius: 14px; padding: 0.9rem 1.05rem; border: 1px solid var(--line);
    background: #FFFFFF; font-size: 0.92rem; line-height: 1.45;
}
.callout-warn { background: #FFF6E3; border-color: #EED9A8; color: #6B4E11; }
.callout-ok { background: #EAF5EF; border-color: #BFDDCD; color: #1F5A42; }
.callout-danger { background: #FCEBEE; border-color: #EFC3CB; color: #82142A; }
.callout-info { background: #EDF3FA; border-color: #C6D8EC; color: #1B3E63; }
.callout b { color: inherit; }
.callout-title { font-weight: 700; margin-bottom: 0.25rem; }

/* ---------------- Cites ---------------- */
.quote {
    background: #FFFFFF; border: 1px solid var(--line); border-left: 4px solid var(--gold);
    border-radius: 10px; padding: 0.7rem 0.9rem; margin-bottom: 0.55rem;
}
.quote-text { font-size: 0.92rem; color: var(--ink); font-style: italic; line-height: 1.45; }
.quote-meta { font-size: 0.73rem; color: var(--muted); margin-top: 0.35rem; }

/* ---------------- Alertes ---------------- */
.alert-item {
    display: flex; gap: 0.6rem; align-items: flex-start;
    background: #FFF6E3; border: 1px solid #EED9A8; border-radius: 12px;
    padding: 0.7rem 0.9rem; margin-bottom: 0.5rem; color: #6B4E11;
    font-size: 0.9rem;
}
.alert-dot {
    width: 8px; height: 8px; border-radius: 50%; background: var(--red);
    margin-top: 0.45rem; flex: 0 0 auto;
}
.hint { font-size: 0.8rem; color: var(--muted); }

/* ---------------- Streamlit widgets ---------------- */
.stButton > button {
    border-radius: 10px; font-weight: 600; border: 1px solid var(--navy);
    padding: 0.45rem 1.1rem; transition: all 0.15s ease;
}
.stButton > button[kind="primary"] {
    background: var(--navy); color: #FFFFFF; border: 1px solid var(--navy);
    box-shadow: 0 6px 16px rgba(11,31,58,0.18);
}
.stButton > button[kind="primary"]:hover {
    background: #16395F; border-color: #16395F; transform: translateY(-1px);
}
.stButton > button[kind="secondary"] {
    background: #FFFFFF; color: var(--navy); border: 1px solid #C9D3DF;
}
.stButton > button[kind="secondary"]:hover { border-color: var(--gold); color: #7A5410; }

[data-testid="stForm"] {
    background: #FFFFFF; border: 1px solid var(--line); border-radius: 16px;
    padding: 1rem 1.2rem;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
textarea {
    border-radius: 10px !important;
}

[data-testid="stDataFrame"], [data-testid="stDataEditor"] {
    border-radius: 12px; overflow: hidden; border: 1px solid var(--line);
}

[data-testid="stExpander"] {
    border: 1px solid var(--line); border-radius: 12px; background: #FFFFFF;
}

hr { border-color: var(--line); }

/* Amaga la barra d'eines de Streamlit (Stop / Deploy) durant la demo */
[data-testid="stToolbar"] { display: none; }
</style>
"""


def injecta_css() -> None:
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Components
# ---------------------------------------------------------------------------


def marca() -> None:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-star">✦</div>
            <div>
                <div class="brand-name">Escolta</div>
                <div class="brand-sub">Damm · UAB The Hack 2026</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def hero(kicker: str, titol: str, text: str, badges: list[str] | None = None) -> None:
    badges_html = ""
    if badges:
        badges_html = (
            '<div class="hero-badges">'
            + "".join(f'<span class="hero-badge">{b}</span>' for b in badges)
            + "</div>"
        )
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-kicker">{kicker}</div>
            <div class="hero-title">{titol}</div>
            <div class="hero-text">{text}</div>
            {badges_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def metrica(valor: str, etiqueta: str, detall: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric">
            <div class="metric-value">{valor}</div>
            <div class="metric-label">{etiqueta}</div>
            <div class="metric-detail">{detall}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def seccio(kicker: str, titol: str, subtitol: str = "") -> None:
    st.markdown(
        f"""
        <div>
            <div class="section-kicker">{kicker}</div>
            <div class="section-title">{titol}</div>
            <div class="section-sub">{subtitol}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def pill(text: str, kind: str = "grey") -> str:
    return f'<span class="pill pill-{kind}">{text}</span>'


def callout(titol: str, text: str, kind: str = "info") -> None:
    st.markdown(
        f"""
        <div class="callout callout-{kind}">
            <div class="callout-title">{titol}</div>
            <div>{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def cicle_escolta(pas_actiu: int = 0) -> None:
    passos = [
        "Necessitat",
        "Consulta IA",
        "Validació",
        "Publicació",
        "Participació",
        "Anàlisi",
        "Visualització",
        "Acció",
    ]
    html = '<div class="cycle">'
    for i, p in enumerate(passos, start=1):
        actiu = i <= pas_actiu
        estil = "background:#0B1F3A;color:#fff;border-color:#0B1F3A;" if actiu else ""
        estil_num = "background:#D9A441;color:#0B1F3A;" if actiu else ""
        estil_text = "color:#fff;" if actiu else ""
        html += (
            f'<div class="cycle-step" style="{estil}">'
            f'<div class="cycle-num" style="{estil_num}">{i}</div>'
            f'<div class="cycle-label" style="{estil_text}">{p}</div>'
            f"</div>"
        )
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def cita(text: str, meta: str) -> None:
    st.markdown(
        f"""
        <div class="quote">
            <div class="quote-text">“{text}”</div>
            <div class="quote-meta">{meta}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def alerta(text: str) -> None:
    st.markdown(
        f'<div class="alert-item"><div class="alert-dot"></div><div>{text}</div></div>',
        unsafe_allow_html=True,
    )
