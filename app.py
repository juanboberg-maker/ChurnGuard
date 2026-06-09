import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
import json

st.set_page_config(
    page_title="ChurnGuard · AI Churn Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Sora:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"], [class*="st-"] { font-family: 'Inter', sans-serif !important; }
.main { background: #060c18; }
.main .block-container { padding: 2.5rem 3rem 5rem; max-width: 1200px; }
section[data-testid="stMain"] > div { background: #060c18; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #1a2e4a; border-radius: 99px; }

[data-testid="stSidebar"] {
    background: #030810 !important;
    border-right: 1px solid rgba(82,167,255,0.07) !important;
    width: 230px !important;
}
[data-testid="stSidebar"] > div:first-child { padding: 0; }
[data-testid="stSidebar"] * { color: #7a9cbe !important; }
[data-testid="stSidebar"] .stRadio > label { visibility: hidden; height: 0; margin: 0; padding: 0; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
    display: flex; flex-direction: column; gap: 1px;
}
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] {
    padding: 0.5rem 1.1rem !important;
    border-radius: 7px; margin: 0 0.65rem;
    transition: all 0.15s; cursor: pointer;
    border-left: 2px solid transparent !important;
}
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"]:hover {
    background: rgba(82,167,255,0.05) !important;
}
[data-testid="stSidebar"] .stRadio label[aria-checked="true"] {
    background: rgba(82,167,255,0.09) !important;
    border-left-color: #52a7ff !important;
}
[data-testid="stSidebar"] .stRadio label[aria-checked="true"] p {
    color: #b8d4f5 !important; font-weight: 500 !important;
}
[data-testid="stSidebar"] .stRadio label p {
    font-size: 0.8rem !important; letter-spacing: 0.01em; margin: 0 !important;
}

h1, h2, h3, h4 {
    font-family: 'Sora', sans-serif !important;
    color: #dce9ff !important; letter-spacing: -0.025em;
}
p, span, li, td, th { color: #7a9cbe; }
hr { border: none !important; border-top: 1px solid rgba(82,167,255,0.08) !important; margin: 2.25rem 0 !important; }

[data-testid="metric-container"] {
    background: #080f1e;
    border: 1px solid rgba(82,167,255,0.11);
    border-top: 1px solid rgba(82,167,255,0.22);
    border-radius: 14px; padding: 1.25rem 1.5rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
    position: relative; overflow: hidden;
}
[data-testid="metric-container"]::after {
    content: '';
    position: absolute; top: 0; left: 20%; right: 20%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(82,167,255,0.35), transparent);
}
[data-testid="metric-container"]:hover {
    border-color: rgba(82,167,255,0.22);
    box-shadow: 0 0 28px rgba(82,167,255,0.06);
}
[data-testid="metric-container"] label {
    font-size: 0.66rem !important; font-weight: 600 !important;
    letter-spacing: 0.11em !important; text-transform: uppercase !important;
    color: #2e5070 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Sora', sans-serif !important; font-size: 1.85rem !important;
    font-weight: 700 !important; color: #dce9ff !important;
}
[data-testid="stMetricDelta"] { font-size: 0.7rem !important; font-weight: 500 !important; }

[data-testid="stButton"] button, [data-testid="stFormSubmitButton"] button {
    background: rgba(82,167,255,0.12) !important;
    color: #93c5fd !important;
    border: 1px solid rgba(82,167,255,0.22) !important;
    border-radius: 9px !important;
    font-family: 'Sora', sans-serif !important;
    font-weight: 600 !important; font-size: 0.88rem !important;
    padding: 0.62rem 2rem !important; letter-spacing: 0.04em;
    transition: all 0.18s ease;
}
[data-testid="stButton"] button:hover, [data-testid="stFormSubmitButton"] button:hover {
    background: rgba(82,167,255,0.2) !important;
    border-color: rgba(82,167,255,0.4) !important;
    color: #bfdbfe !important;
    box-shadow: 0 0 20px rgba(82,167,255,0.15) !important;
    transform: translateY(-1px);
}
[data-testid="stFormSubmitButton"] button {
    background: rgba(82,167,255,0.14) !important;
    border-color: rgba(82,167,255,0.3) !important;
    font-size: 0.92rem !important; padding: 0.7rem 2.5rem !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(82,167,255,0.09) !important; gap: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; border: none !important;
    color: #3a6080 !important; font-size: 0.8rem !important;
    font-weight: 500 !important; letter-spacing: 0.04em !important;
    padding: 0.65rem 1.3rem !important;
    border-bottom: 2px solid transparent !important; transition: all 0.15s;
}
.stTabs [data-baseweb="tab"]:hover { color: #7aadcc !important; }
.stTabs [aria-selected="true"] { color: #52a7ff !important; border-bottom-color: #52a7ff !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 1.75rem; }

[data-testid="stDataFrame"] {
    border-radius: 12px; overflow: hidden;
    border: 1px solid rgba(82,167,255,0.09);
}

[data-testid="stSelectbox"] > div > div,
[data-testid="stNumberInput"] > div > div > input {
    background: #080f1e !important; border-color: rgba(82,167,255,0.13) !important;
    color: #a8c4e0 !important; border-radius: 8px !important;
    font-size: 0.85rem !important;
}

[data-testid="stAlert"] { border-radius: 12px !important; border: 1px solid !important; }
.stSuccess { background: rgba(52,211,153,0.06) !important; border-color: rgba(52,211,153,0.22) !important; }
.stError   { background: rgba(239,68,68,0.06) !important;  border-color: rgba(239,68,68,0.22) !important; }

[data-testid="stForm"] label, .stSelectbox label,
.stSlider label, .stNumberInput label {
    font-size: 0.75rem !important; color: #3a6080 !important;
    font-weight: 500 !important; letter-spacing: 0.02em !important;
}

.badge {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 11px; border-radius: 999px;
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.07em;
    text-transform: uppercase; font-family: 'Inter', sans-serif;
}
.badge-blue   { background: rgba(82,167,255,0.1);  color: #7ab8f5; border: 1px solid rgba(82,167,255,0.18); }
.badge-red    { background: rgba(239,68,68,0.1);   color: #fca5a5; border: 1px solid rgba(239,68,68,0.22); }
.badge-green  { background: rgba(52,211,153,0.1);  color: #6ee7b7; border: 1px solid rgba(52,211,153,0.22); }
.badge-amber  { background: rgba(245,158,11,0.1);  color: #fcd34d; border: 1px solid rgba(245,158,11,0.22); }
.badge-purple { background: rgba(139,92,246,0.1);  color: #c4b5fd; border: 1px solid rgba(139,92,246,0.22); }
.badge-cyan   { background: rgba(34,211,238,0.08); color: #67e8f9; border: 1px solid rgba(34,211,238,0.18); }

.risk-pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 5px 13px; border-radius: 999px;
    font-size: 0.72rem; font-weight: 600;
    background: rgba(239,68,68,0.09); color: #fca5a5;
    border: 1px solid rgba(239,68,68,0.22); margin: 3px 4px 3px 0;
    letter-spacing: 0.02em;
}

.stat-card {
    background: #080f1e;
    border: 1px solid rgba(82,167,255,0.1);
    border-radius: 16px; padding: 1.6rem 1.5rem;
    position: relative; overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
}
.stat-card:hover { border-color: rgba(82,167,255,0.24); transform: translateY(-2px); }
.stat-card::before {
    content: '';
    position: absolute; top: 0; left: 15%; right: 15%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(82,167,255,0.28), transparent);
}
.stat-card .sc-label {
    font-size: 0.65rem; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: #2e5070; margin-bottom: 0.6rem;
}
.stat-card .sc-value {
    font-family: 'Sora', sans-serif; font-size: 2.3rem; font-weight: 700;
    color: #dce9ff; line-height: 1; margin-bottom: 0.35rem;
}
.stat-card .sc-sub { font-size: 0.73rem; color: #2e5070; line-height: 1.5; }

.icard {
    background: #07111f;
    border: 1px solid rgba(82,167,255,0.09);
    border-radius: 13px; padding: 1.2rem 1.3rem 1.2rem 1.5rem;
    margin-bottom: 0.7rem; transition: border-color 0.2s;
    position: relative;
}
.icard:hover { border-color: rgba(82,167,255,0.2); }
.icard .ic-accent {
    width: 3px; height: calc(100% - 24px);
    position: absolute; left: 0; top: 12px; border-radius: 0 3px 3px 0;
}
.icard .ic-title {
    font-family: 'Sora', sans-serif; font-size: 0.85rem;
    font-weight: 600; color: #b8d4f5; margin-bottom: 0.35rem;
}
.icard .ic-body { font-size: 0.8rem; color: #3d6585; line-height: 1.65; }
.icard code {
    font-family: 'JetBrains Mono', monospace; font-size: 0.76rem;
    background: rgba(82,167,255,0.08); color: #7ab8f5;
    padding: 1px 5px; border-radius: 4px;
}

.cost-card {
    background: #07111f;
    border: 1px solid rgba(82,167,255,0.09);
    border-radius: 14px; padding: 1.5rem 1.25rem;
    text-align: center;
    transition: border-color 0.2s, transform 0.18s;
    position: relative; overflow: hidden;
}
.cost-card::before {
    content: '';
    position: absolute; top: 0; left: 25%; right: 25%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(82,167,255,0.22), transparent);
}
.cost-card:hover { border-color: rgba(82,167,255,0.22); transform: translateY(-2px); }
.cost-card .cc-label {
    font-size: 0.63rem; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: #2e5070; margin-bottom: 0.55rem;
}
.cost-card .cc-value {
    font-family: 'Sora', sans-serif; font-size: 2.2rem; font-weight: 700;
    line-height: 1; margin-bottom: 0.4rem;
}
.cost-card .cc-desc { font-size: 0.73rem; color: #2e5070; line-height: 1.55; }

.hero-wrapper {
    background: #07111f;
    border: 1px solid rgba(82,167,255,0.09);
    border-radius: 20px; padding: 3.25rem 3.75rem;
    margin-bottom: 2rem; position: relative; overflow: hidden;
}
.hero-wrapper::before {
    content: '';
    position: absolute; right: -80px; top: -80px;
    width: 320px; height: 320px; border-radius: 50%;
    background: radial-gradient(circle, rgba(82,167,255,0.05) 0%, transparent 70%);
    pointer-events: none;
}
.hero-wrapper::after {
    content: '';
    position: absolute; top: 0; left: 15%; right: 15%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(82,167,255,0.22), transparent);
}
.hero-label {
    font-size: 0.68rem; font-weight: 600; letter-spacing: 0.14em;
    text-transform: uppercase; color: #52a7ff;
    margin-bottom: 1rem; display: flex; align-items: center; gap: 8px;
}
.hero-label::before {
    content: '';
    display: inline-block; width: 20px; height: 1px; background: #52a7ff;
}
.hero-title {
    font-family: 'Sora', sans-serif; font-size: 2.8rem; font-weight: 800;
    color: #dce9ff; line-height: 1.08; letter-spacing: -0.035em;
    margin-bottom: 0.85rem;
}
.hero-title .accent { color: #52a7ff; }
.hero-title .accent-red { color: #f87171; }
.hero-sub {
    font-size: 0.95rem; color: #3d6585; line-height: 1.7;
    max-width: 540px; margin-bottom: 1.75rem;
}
.hero-tag-row { display: flex; gap: 8px; flex-wrap: wrap; }

.result-panel {
    border-radius: 15px; padding: 1.85rem 2rem; border: 1px solid;
}
.result-panel.danger { background: rgba(239,68,68,0.05); border-color: rgba(239,68,68,0.2); }
.result-panel.safe   { background: rgba(52,211,153,0.05); border-color: rgba(52,211,153,0.2); }
.result-panel .rp-label {
    font-size: 0.65rem; font-weight: 600; letter-spacing: 0.12em;
    text-transform: uppercase; margin-bottom: 0.4rem;
}
.result-panel.danger .rp-label { color: #7f2020; }
.result-panel.safe .rp-label   { color: #1a5c40; }
.result-panel .rp-title {
    font-family: 'Sora', sans-serif; font-size: 1.1rem;
    font-weight: 700; margin-bottom: 0.6rem;
}
.result-panel.danger .rp-title { color: #f87171; }
.result-panel.safe .rp-title   { color: #34d399; }
.result-panel .rp-prob {
    font-family: 'JetBrains Mono', monospace; font-size: 3rem;
    font-weight: 500; line-height: 1; margin-bottom: 0.65rem;
}
.result-panel.danger .rp-prob { color: #f87171; }
.result-panel.safe .rp-prob   { color: #34d399; }
.result-panel .rp-body { font-size: 0.8rem; color: #3d6585; line-height: 1.65; }
.result-panel .rp-divider { border: none; border-top: 1px solid rgba(255,255,255,0.05); margin: 1rem 0; }

.form-section-header {
    display: flex; align-items: center; gap: 8px;
    font-family: 'Sora', sans-serif; font-size: 0.75rem;
    font-weight: 600; letter-spacing: 0.09em; text-transform: uppercase;
    color: #2e5070; margin-bottom: 1.1rem; padding-bottom: 0.55rem;
    border-bottom: 1px solid rgba(82,167,255,0.07);
}

.sb-logo {
    padding: 1.85rem 1.5rem 1.35rem;
    border-bottom: 1px solid rgba(82,167,255,0.06); margin-bottom: 0.5rem;
}
.sb-logo-title {
    font-family: 'Sora', sans-serif; font-size: 1.05rem;
    font-weight: 800; color: #dce9ff; letter-spacing: -0.01em;
    display: flex; align-items: center; gap: 7px;
}
.sb-logo-sub {
    font-size: 0.63rem; color: #1a3a55; letter-spacing: 0.09em;
    text-transform: uppercase; margin-top: 4px; padding-left: 1px;
}
.sb-status {
    margin: 0.65rem 0.75rem 0;
    background: rgba(82,167,255,0.03);
    border: 1px solid rgba(82,167,255,0.07);
    border-radius: 10px; padding: 0.85rem 1rem;
}
.sb-status-title {
    font-size: 0.61rem; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; color: #1a3a55; margin-bottom: 0.65rem;
}
.sb-status-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.22rem 0; font-size: 0.7rem;
}
.sb-status-row .sk { color: #2e5070; }
.sb-status-row .sv {
    color: #52a7ff; font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem; font-weight: 500;
}
.sb-dot {
    display: inline-block; width: 6px; height: 6px; border-radius: 50%;
    background: #34d399; margin-right: 5px;
    box-shadow: 0 0 6px rgba(52,211,153,0.6);
}
.sb-footer { margin: 1.5rem 1rem 0; font-size: 0.62rem; color: #142030; line-height: 1.7; }

.section-eyebrow {
    font-size: 0.65rem; font-weight: 600; letter-spacing: 0.13em;
    text-transform: uppercase; color: #2e5070;
}
.section-title {
    font-family: 'Sora', sans-serif; font-size: 1.75rem; font-weight: 700;
    color: #dce9ff; letter-spacing: -0.025em; margin: 0.4rem 0 0.4rem; line-height: 1.15;
}
.section-subtitle { font-size: 0.87rem; color: #2e5070; margin-bottom: 1.85rem; line-height: 1.6; }
.section-header-block { margin-bottom: 1.75rem; }

.conclusion-banner {
    background: #07111f;
    border: 1px solid rgba(82,167,255,0.14);
    border-radius: 20px; padding: 3.5rem 2.5rem;
    text-align: center; position: relative; overflow: hidden; margin-top: 1.25rem;
}
.conclusion-banner::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(82,167,255,0.06) 0%, transparent 60%);
    pointer-events: none;
}
.conclusion-banner::after {
    content: '';
    position: absolute; top: 0; left: 20%; right: 20%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(82,167,255,0.3), transparent);
}
.conclusion-banner .cb-eyebrow {
    font-size: 0.65rem; font-weight: 600; letter-spacing: 0.13em;
    text-transform: uppercase; color: #2e5070; margin-bottom: 0.9rem;
}
.conclusion-banner .cb-title {
    font-family: 'Sora', sans-serif; font-size: 1.7rem;
    font-weight: 700; color: #dce9ff; margin-bottom: 0.55rem; line-height: 1.2;
}
.conclusion-banner .cb-number { color: #52a7ff; }
.conclusion-banner .cb-sub { font-size: 0.82rem; color: #1e3d58; margin-top: 0.85rem; }
</style>
""", unsafe_allow_html=True)

DARK_BG  = "#060c18"
PLOT_BG  = "#07111f"
GRID_COL = "rgba(82,167,255,0.06)"
LINE_COL = "rgba(82,167,255,0.1)"

PLOT_LAYOUT = dict(
    font=dict(family="Inter", color="#3d6585", size=12),
    plot_bgcolor=PLOT_BG, paper_bgcolor=DARK_BG,
    margin=dict(t=44, b=40, l=48, r=32),
    xaxis=dict(showgrid=True, gridcolor=GRID_COL, linecolor=LINE_COL, zeroline=False, tickfont=dict(size=11)),
    yaxis=dict(showgrid=True, gridcolor=GRID_COL, linecolor=LINE_COL, zeroline=False, tickfont=dict(size=11)),
    hoverlabel=dict(bgcolor="#0a1828", font_size=12, font_family="Inter", bordercolor="rgba(82,167,255,0.18)"),
    colorway=["#52a7ff", "#f87171", "#34d399", "#fcd34d", "#c4b5fd"],
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#3d6585", size=11)),
)

C = {
    "churn":    "#f87171",
    "no_churn": "#52a7ff",
    "accent":   "#52a7ff",
    "muted":    "#2e5070",
    "success":  "#34d399",
    "warning":  "#fcd34d",
    "purple":   "#c4b5fd",
}

@st.cache_resource
def cargar_modelo():
    with open("model/model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("model/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("model/features.pkl", "rb") as f:
        features = pickle.load(f)
    return model, scaler, features

model, scaler, features = cargar_modelo()

with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <div class="sb-logo-title">🛡️ ChurnGuard</div>
        <div class="sb-logo-sub">AI Churn Intelligence</div>
        <div style="font-size:0.58rem; color:#1a3a55; letter-spacing:0.04em; margin-top:4px; padding-left:1px;">por Juan Boberg Aguirre</div>
    </div>
    """, unsafe_allow_html=True)

    pagina = st.radio(
        "nav",
        [
            "01 · El Problema",
            "02 · Los Datos",
            "03 · El Modelo",
            "04 · Resultados",
            "05 · Predicción en Vivo",
            "06 · Conclusiones",
        ],
        label_visibility="collapsed",
    )

    st.markdown("""
    <div style="height: 1.5rem;"></div>
    <div class="sb-status">
        <div class="sb-status-title"><span class="sb-dot"></span>Estado del modelo</div>
        <div class="sb-status-row"><span class="sk">Dataset</span><span class="sv">IBM Telco</span></div>
        <div class="sb-status-row"><span class="sk">Algoritmo</span><span class="sv">Logistic Reg.</span></div>
        <div class="sb-status-row"><span class="sk">AUC-ROC</span><span class="sv">0.844</span></div>
        <div class="sb-status-row"><span class="sk">Threshold</span><span class="sv">0.30</span></div>
        <div class="sb-status-row"><span class="sk">Recall</span><span class="sv">92.7 %</span></div>
    </div>
    <div class="sb-footer">Bootcamp Data Analytics · 2024</div>
    """, unsafe_allow_html=True)

def page_header(eyebrow: str, title: str, subtitle: str = ""):
    sub_html = f'<div class="section-subtitle">{subtitle}</div>' if subtitle else ""
    st.markdown(f"""
    <div class="section-header-block">
        <div class="section-eyebrow">{eyebrow}</div>
        <div class="section-title">{title}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)

def icard(title: str, body: str, color: str = "#52a7ff"):
    st.markdown(f"""
    <div class="icard">
      <div class="ic-accent" style="background:{color};"></div>
      <div class="ic-title">{title}</div>
      <div class="ic-body">{body}</div>
    </div>
    """, unsafe_allow_html=True)

def eyebrow(text: str, mb: str = "1rem"):
    st.markdown(f'<div class="section-eyebrow" style="margin-bottom:{mb};">{text}</div>', unsafe_allow_html=True)

# ── 01 EL PROBLEMA ────────────────────────────────────────────────────────────
if pagina == "01 · El Problema":
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero-label">Churn Intelligence · IBM Telco</div>
        <div class="hero-title">
            Retener clientes<br>antes de que <span class="accent-red">se vayan.</span>
        </div>
        <div class="hero-sub">
            ChurnGuard es un sistema de inteligencia predictiva para detección temprana de abandono
            de clientes en telecomunicaciones. Entrenado sobre el dataset IBM Telco, detecta el
            <strong style="color:#52a7ff;">92.7 %</strong> de los clientes en riesgo
            antes de que abandonen — maximizando recall frente a un ratio de coste 40:1.
        </div>
        <div class="hero-tag-row">
            <span class="badge badge-blue">🛡️ IBM Telco Dataset</span>
            <span class="badge badge-purple">Logistic Regression</span>
            <span class="badge badge-green">AUC 0.844</span>
            <span class="badge badge-amber">Recall 92.7 %</span>
            <span class="badge badge-cyan">Threshold 0.30</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="cost-card">
            <div class="cc-label">Tasa de churn</div>
            <div class="cc-value" style="color:#52a7ff;">26.5 %</div>
            <div class="cc-desc">1.869 clientes en riesgo<br>sobre 7.043 en el dataset</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="cost-card">
            <div class="cc-label">Coste · Falso Negativo</div>
            <div class="cc-value" style="color:#f87171;">200 €</div>
            <div class="cc-desc">Cliente perdido sin retención<br>coste directo por churner</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="cost-card">
            <div class="cc-label">Coste · Falso Positivo</div>
            <div class="cc-value" style="color:#fcd34d;">5 €</div>
            <div class="cc-desc">Llamada innecesaria de retención<br>ratio FN/FP = <strong style="color:#fcd34d;">40:1</strong></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()
    eyebrow("Por qué existe ChurnGuard", "1.25rem")

    col1, col2 = st.columns(2)
    with col1:
        icard("Ratio de coste 40:1",
              "Un falso negativo cuesta 40 veces más que un falso positivo. Cada cliente que se va sin ser detectado representa 200 € de margen perdido frente a los 5 € de una retención innecesaria.",
              C["churn"])
        icard("Objetivo: maximizar Recall",
              "ChurnGuard ajusta el umbral de decisión a 0.30 para capturar el 92.7 % de los churners, asumiendo conscientemente un mayor número de falsos positivos.",
              C["accent"])
    with col2:
        icard("Modelo interpretable por diseño",
              "A diferencia de Gradient Boosting (caja negra), Logistic Regression permite explicar exactamente qué variables impulsan el riesgo de cada cliente.",
              C["purple"])
        icard("Beneficio neto estimado: 101.800 €",
              f'Con 521 churners detectados de 561 reales, el modelo genera un beneficio neto de <strong style="color:{C["success"]};">101.800 €</strong> por cada ciclo de retención ejecutado.',
              C["success"])

# ── 02 LOS DATOS ──────────────────────────────────────────────────────────────
elif pagina == "02 · Los Datos":
    page_header("02 · Dataset", "Exploración de datos",
                "IBM Telco Customer Churn — 7.043 registros · 21 variables")

    @st.cache_data
    def load_data():
        return pd.read_csv("data/telco_churn.csv")
    df = load_data()

    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("Total clientes", f"{df.shape[0]:,}")
    with m2:
        churn_pct = df["Churn"].value_counts()["Yes"] / df.shape[0] * 100
        st.metric("Tasa de churn", f"{churn_pct:.1f} %")
    with m3: st.metric("Churners", f"{df['Churn'].value_counts()['Yes']:,}")
    with m4: st.metric("Variables", df.shape[1])

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["  📋  Vista del dataset  ", "  📊  Distribución de churn  "])

    with tab1:
        st.dataframe(df.head(25), use_container_width=True, hide_index=True)

    with tab2:
        conteo = df["Churn"].value_counts().reset_index()
        conteo.columns = ["Churn", "count"]
        conteo["pct"] = (conteo["count"] / conteo["count"].sum() * 100).round(1)
        col_a, col_b = st.columns([1.5, 1])
        with col_a:
            fig = px.bar(conteo, x="Churn", y="count", color="Churn",
                         color_discrete_map={"Yes": C["churn"], "No": C["no_churn"]},
                         labels={"count": "Clientes", "Churn": ""},
                         text=conteo.apply(lambda r: f"{r['count']:,}  ({r['pct']}%)", axis=1))
            fig.update_traces(textposition="outside", marker_line_width=0,
                              textfont=dict(size=12, color="#7a9cbe"))
            fig.update_layout(**PLOT_LAYOUT, showlegend=False,
                              yaxis_title="Número de clientes", bargap=0.5)
            st.plotly_chart(fig, use_container_width=True)
        with col_b:
            st.markdown("<br>", unsafe_allow_html=True)
            icard("Desbalance de clases",
                  "73.5 % no churners vs 26.5 % churners. Este desbalance refuerza la necesidad de optimizar el threshold.", C["churn"])
            icard("1 de cada 4 clientes abandona",
                  f'Sobre 7.043 clientes, esto representa <strong style="color:{C["churn"]};">1.869 churners</strong> en el dataset.', C["warning"])

# ── 03 EL MODELO ──────────────────────────────────────────────────────────────
elif pagina == "03 · El Modelo":
    page_header("03 · Modelado", "Selección del algoritmo",
                "Comparativa sobre IBM Telco — clase Churn = Yes · threshold por defecto 0.50")

    resultados = {
        "Modelo":    ["Logistic Regression ✓", "Random Forest", "AdaBoost", "Gradient Boosting"],
        "Precision": [0.66, 0.65, 0.51, 0.52],
        "Recall":    [0.42, 0.50, 0.77, 0.82],
        "F1":        [0.51, 0.57, 0.61, 0.64],
        "Accuracy":  [0.79, 0.80, 0.74, 0.75],
    }
    df_modelos = pd.DataFrame(resultados)

    def highlight_lr(row):
        if "✓" in str(row["Modelo"]):
            return ["background-color: rgba(82,167,255,0.08); color: #7ab8f5; font-weight:600"] * len(row)
        return ["color: #3d6585"] * len(row)

    tab_t, tab_c = st.tabs(["  📊  Tabla comparativa  ", "  📈  Visualización  "])
    with tab_t:
        st.dataframe(df_modelos.style.apply(highlight_lr, axis=1)
                     .format({"Precision": "{:.2f}", "Recall": "{:.2f}", "F1": "{:.2f}", "Accuracy": "{:.2f}"}),
                     use_container_width=True, hide_index=True)
    with tab_c:
        metrics = ["Precision", "Recall", "F1", "Accuracy"]
        df_melt = df_modelos.melt(id_vars="Modelo", value_vars=metrics, var_name="Métrica", value_name="Valor")
        fig_m = px.line(df_melt, x="Métrica", y="Valor", color="Modelo", markers=True,
                        color_discrete_sequence=["#52a7ff", "#3a6585", "#1e3a55", "#0f2035"])
        fig_m.update_traces(line_width=2.5, marker_size=7)
        fig_m.update_layout(**PLOT_LAYOUT, yaxis_range=[0.35, 0.9])
        st.plotly_chart(fig_m, use_container_width=True)

    st.divider()
    eyebrow("Justificación de la elección", "1.25rem")
    jc1, jc2, jc3 = st.columns(3)
    with jc1:
        icard("Interpretabilidad total",
              "Cada coeficiente explica cuánto empuja una variable hacia el churn. Con Gradient Boosting el modelo es una caja negra.", C["accent"])
    with jc2:
        icard("Recall equivalente con threshold 0.30",
              f'Gradient Boosting: 0.82 con threshold 0.50. Logistic Regression: <strong style="color:{C["accent"]};">0.927</strong> con threshold 0.30.', C["warning"])
    with jc3:
        icard("Validado por GridSearchCV",
              "25 combinaciones en 5 folds confirman <code>C=1</code> como parámetro óptimo.", C["success"])

# ── 04 RESULTADOS ─────────────────────────────────────────────────────────────
elif pagina == "04 · Resultados":
    page_header("04 · Evaluación", "Resultados del modelo",
                "Logistic Regression · threshold optimizado a 0.30 · coste FN/FP = 40:1")

    with open("model/roc_data.json", "r") as f:
        roc_data = json.load(f)

    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("AUC-ROC", "0.844", delta="Discriminación alta")
    with m2: st.metric("Recall", "0.927", delta="+48.5 pp vs default", delta_color="normal")
    with m3: st.metric("Threshold", "0.30", delta="Optimizado por coste", delta_color="normal")
    with m4: st.metric("Beneficio neto", "101.800 €", delta="vs 0 € sin modelo", delta_color="normal")

    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["  📈  Curva ROC  ", "  ⚖️  Impacto del Threshold  "])

    with tab1:
        col_r, col_t = st.columns([1.6, 1])
        with col_r:
            fig_roc = go.Figure()
            fig_roc.add_trace(go.Scatter(
                x=roc_data["fpr"], y=roc_data["tpr"],
                fill="tozeroy", fillcolor="rgba(82,167,255,0.04)",
                line=dict(color=C["accent"], width=2.5),
                name=f"AUC = {roc_data['auc']:.3f}",
            ))
            fig_roc.add_shape(type="line", line=dict(dash="dot", color=C["muted"], width=1),
                              x0=0, x1=1, y0=0, y1=1)
            fig_roc.update_layout(**PLOT_LAYOUT,
                                  xaxis_title="Tasa de Falsos Positivos (FPR)",
                                  yaxis_title="Tasa de Verdaderos Positivos (TPR)")
            st.plotly_chart(fig_roc, use_container_width=True)
        with col_t:
            st.markdown("<br>", unsafe_allow_html=True)
            icard("AUC = 0.844", "El área bajo la curva ROC indica discriminación alta. Un clasificador aleatorio obtendría 0.50.", C["accent"])
            icard("La curva se aleja del azar", "Cuanto más alejada esté la curva ROC, mayor es el poder predictivo del modelo.", C["muted"])

    with tab2:
        threshold_data = {
            "Threshold":           ["0.50  (defecto)", "0.30  (optimizado)"],
            "Recall":              [0.42, 0.927],
            "Precision":           [0.66, 0.429],
            "Churners detectados": [236, 521],
            "FP (llamadas extra)": [122, 693],
            "Beneficio neto":      ["—", "101.800 €"],
        }
        df_thr = pd.DataFrame(threshold_data)

        def hl_opt(row):
            if "optimizado" in row["Threshold"]:
                return ["background-color: rgba(82,167,255,0.08); color:#7ab8f5; font-weight:600"] * len(row)
            return ["color:#3d6585"] * len(row)

        st.dataframe(df_thr.style.apply(hl_opt, axis=1), use_container_width=True, hide_index=True)
        st.markdown("<br>", unsafe_allow_html=True)

        fig_compare = go.Figure()
        fig_compare.add_trace(go.Bar(
            x=["Threshold 0.50", "Threshold 0.30"], y=[236, 521],
            marker_color=[C["muted"], C["churn"]],
            text=[236, 521], textposition="outside",
            textfont=dict(color="#7a9cbe", size=13), marker_line_width=0,
        ))
        fig_compare.update_layout(**PLOT_LAYOUT, showlegend=False,
                                  yaxis_title="Churners detectados", bargap=0.5)
        st.plotly_chart(fig_compare, use_container_width=True)

# ── 05 PREDICCIÓN EN VIVO ─────────────────────────────────────────────────────
elif pagina == "05 · Predicción en Vivo":
    page_header("05 · Live Inference", "Predicción en tiempo real",
                "Introduce los datos del cliente para evaluar su riesgo de abandono.")

    with st.form("predict_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown('<div class="form-section-header">👤 Perfil del cliente</div>', unsafe_allow_html=True)
            gender          = st.selectbox("Género",              ["Female", "Male"])
            SeniorCitizen   = st.selectbox("Senior Citizen",      [0, 1], format_func=lambda x: "Sí" if x else "No")
            Partner         = st.selectbox("Pareja",              ["Yes", "No"])
            Dependents      = st.selectbox("Dependientes",        ["Yes", "No"])
            tenure          = st.slider("Meses como cliente",     0, 72, 12)
            PhoneService    = st.selectbox("Servicio telefónico", ["Yes", "No"])

        with col2:
            st.markdown('<div class="form-section-header">📡 Servicios contratados</div>', unsafe_allow_html=True)
            MultipleLines    = st.selectbox("Múltiples líneas",       ["No phone service", "No", "Yes"])
            InternetService  = st.selectbox("Internet",               ["DSL", "Fiber optic", "No"])
            OnlineSecurity   = st.selectbox("Seguridad online",       ["No internet service", "No", "Yes"])
            OnlineBackup     = st.selectbox("Backup online",          ["No internet service", "No", "Yes"])
            DeviceProtection = st.selectbox("Protección dispositivo", ["No internet service", "No", "Yes"])
            TechSupport      = st.selectbox("Soporte técnico",        ["No internet service", "No", "Yes"])

        with col3:
            st.markdown('<div class="form-section-header">💳 Contrato y facturación</div>', unsafe_allow_html=True)
            StreamingTV      = st.selectbox("Streaming TV",           ["No internet service", "No", "Yes"])
            StreamingMovies  = st.selectbox("Streaming películas",    ["No internet service", "No", "Yes"])
            Contract         = st.selectbox("Tipo de contrato",       ["Month-to-month", "One year", "Two year"])
            PaperlessBilling = st.selectbox("Factura digital",        ["Yes", "No"])
            PaymentMethod    = st.selectbox("Método de pago",         [
                "Bank transfer (automatic)", "Credit card (automatic)",
                "Electronic check", "Mailed check",
            ])
            MonthlyCharges   = st.number_input("Cargo mensual (€)",  0.0, 200.0, 50.0, step=0.5)
            TotalCharges     = st.number_input("Cargo total (€)",    0.0, 10000.0, 500.0, step=10.0)

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("  🔮  Analizar riesgo de churn  ", use_container_width=True)

    if submitted:
        input_dict = dict(
            SeniorCitizen=SeniorCitizen, tenure=tenure,
            MonthlyCharges=MonthlyCharges, TotalCharges=TotalCharges,
            gender=gender, Partner=Partner, Dependents=Dependents,
            PhoneService=PhoneService, MultipleLines=MultipleLines,
            InternetService=InternetService, OnlineSecurity=OnlineSecurity,
            OnlineBackup=OnlineBackup, DeviceProtection=DeviceProtection,
            TechSupport=TechSupport, StreamingTV=StreamingTV,
            StreamingMovies=StreamingMovies, Contract=Contract,
            PaperlessBilling=PaperlessBilling, PaymentMethod=PaymentMethod,
        )
        input_df      = pd.DataFrame([input_dict])
        input_encoded = pd.get_dummies(input_df)
        input_aligned = input_encoded.reindex(columns=features, fill_value=0)
        input_scaled  = scaler.transform(input_aligned)
        prob          = model.predict_proba(input_scaled)[0][1]
        pred          = int(prob >= 0.30)

        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()
        eyebrow("Resultado del análisis", "1.25rem")

        gauge_color = C["churn"] if pred == 1 else C["success"]
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=round(prob * 100, 1),
            number=dict(suffix=" %", font=dict(size=46, family="Sora", color=gauge_color)),
            title=dict(text="Probabilidad de Churn", font=dict(size=12, family="Inter", color="#2e5070")),
            gauge=dict(
                axis=dict(range=[0, 100], nticks=6,
                          tickfont=dict(size=10, family="Inter", color="#1a3a55"),
                          tickcolor=LINE_COL),
                bar=dict(color=gauge_color, thickness=0.2),
                bgcolor=PLOT_BG, borderwidth=0,
                steps=[
                    dict(range=[0, 30],   color="rgba(52,211,153,0.05)"),
                    dict(range=[30, 60],  color="rgba(252,211,77,0.04)"),
                    dict(range=[60, 100], color="rgba(248,113,113,0.06)"),
                ],
                threshold=dict(line=dict(color="#dce9ff", width=2), thickness=0.8, value=30),
            ),
        ))
        fig_gauge.update_layout(height=290, margin=dict(t=55, b=10, l=20, r=20),
                                paper_bgcolor=DARK_BG, font_family="Inter")

        gcol1, gcol2 = st.columns([1.1, 1])
        with gcol1:
            st.plotly_chart(fig_gauge, use_container_width=True)
        with gcol2:
            st.markdown("<br>", unsafe_allow_html=True)
            if pred == 1:
                verdict, rp_title, rp_body = "danger", "⚠️ Riesgo alto de churn", \
                    "La probabilidad supera el umbral de decisión (30 %).<br>Se recomienda activar protocolo de retención inmediato."
            else:
                verdict, rp_title, rp_body = "safe", "✓ Cliente estable", \
                    "La probabilidad está por debajo del umbral (30 %).<br>No se requiere acción de retención inmediata."

            st.markdown(f"""
            <div class="result-panel {verdict}">
                <div class="rp-label">Decisión del modelo</div>
                <div class="rp-title">{rp_title}</div>
                <div class="rp-prob">{prob:.1%}</div>
                <hr class="rp-divider">
                <div class="rp-body">{rp_body}</div>
            </div>
            """, unsafe_allow_html=True)

            risk_factors = []
            if Contract == "Month-to-month":        risk_factors.append(("📋", "Contrato mensual"))
            if InternetService == "Fiber optic":    risk_factors.append(("📡", "Fibra óptica"))
            if tenure < 12:                         risk_factors.append(("🕐", "Cliente < 12 m"))
            if PaymentMethod == "Electronic check": risk_factors.append(("💳", "Cheque electrónico"))
            if TechSupport == "No":                 risk_factors.append(("🔧", "Sin soporte técnico"))
            if SeniorCitizen == 1:                  risk_factors.append(("👤", "Senior Citizen"))

            if risk_factors:
                pills_html = "".join(f'<span class="risk-pill">{icon} {label}</span>' for icon, label in risk_factors)
                st.markdown(f"""
                <br>
                <div style="font-size:0.63rem; font-weight:600; letter-spacing:0.11em;
                            text-transform:uppercase; color:#2e5070; margin-bottom:0.6rem;">
                    Factores de riesgo detectados
                </div>
                <div>{pills_html}</div>
                """, unsafe_allow_html=True)

# ── 06 CONCLUSIONES ───────────────────────────────────────────────────────────
elif pagina == "06 · Conclusiones":
    page_header("06 · Cierre", "Decisiones, valor y próximos pasos",
                "Un modelo de negocio primero, técnico segundo.")

    eyebrow("3 decisiones clave", "1.25rem")
    dc1, dc2, dc3 = st.columns(3)
    with dc1:
        icard("Logistic Regression sobre Gradient Boosting",
              "Diferencia de recall de solo 0.01 — 6 clientes sobre 561. A cambio: interpretabilidad total.", C["accent"])
    with dc2:
        icard("Threshold 0.30 sobre 0.50",
              "Con FN = 200 € y FP = 5 € (ratio 40:1), reducir el umbral es una decisión de negocio, no un error técnico.", C["warning"])
    with dc3:
        icard("GridSearchCV como validación científica",
              "25 combinaciones · 5 folds confirman <code>C=1</code> como parámetro óptimo.", C["success"])

    st.divider()
    eyebrow("Limitaciones del modelo", "1.25rem")
    lc1, lc2 = st.columns(2)
    with lc1:
        icard("Dataset estático · 2017", "No captura cambios de comportamiento recientes. Requeriría reentrenamiento periódico.", C["churn"])
        icard("Sin datos cualitativos", "No incluye NPS, tickets de soporte ni satisfacción del cliente.", C["muted"])
    with lc2:
        icard("Churn voluntario vs involuntario", "El modelo no distingue entre abandono voluntario y causas externas.", C["muted"])
        icard("Multicolinealidad leve", "<code>TotalCharges</code> es parcialmente derivada de <code>tenure × MonthlyCharges</code>.", C["warning"])

    st.divider()
    eyebrow("Valor generado", "1.25rem")
    fm1, fm2, fm3 = st.columns(3)
    with fm1:
        st.markdown("""
        <div class="stat-card">
            <div class="sc-label">Churners detectados</div>
            <div class="sc-value">521<span style="font-size:1.1rem; color:#2e5070;"> / 561</span></div>
            <div class="sc-sub">Recall del 92.7 %</div>
        </div>
        """, unsafe_allow_html=True)
    with fm2:
        st.markdown("""
        <div class="stat-card">
            <div class="sc-label">Ahorro en retención</div>
            <div class="sc-value" style="color:#52a7ff;">104.200 €</div>
            <div class="sc-sub">521 clientes × 200 €</div>
        </div>
        """, unsafe_allow_html=True)
    with fm3:
        st.markdown("""
        <div class="stat-card">
            <div class="sc-label">Valor total generado</div>
            <div class="sc-value" style="color:#34d399;">203.010 €</div>
            <div class="sc-sub">Neto tras coste de llamadas</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="conclusion-banner">
        <div class="cb-eyebrow">ChurnGuard · IBM Telco · Logistic Regression · AUC 0.844</div>
        <div class="cb-title">
            🛡️ ChurnGuard detecta el <span class="cb-number">92.7 %</span> de los clientes en riesgo<br>
            antes de que sea demasiado tarde.
        </div>
        <div class="cb-sub">
            Threshold 0.30 · Recall 0.927 · Beneficio neto 101.800 € · Bootcamp Data Analytics 2024
        </div>
    </div>
    """, unsafe_allow_html=True)