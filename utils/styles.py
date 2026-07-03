from html import escape

import streamlit as st

DARK_CSS = """
<style>
/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stSidebar"],
[data-testid="collapsedControl"] { display: none !important; }
.block-container {
    padding-top: 0 !important;
    padding-left: clamp(16px, 2.6vw, 40px) !important;
    padding-right: clamp(16px, 2.6vw, 40px) !important;
    padding-bottom: 28px !important;
    max-width: 1680px !important;
    margin: 0 auto !important;
}
section[data-testid="stMain"] > div:first-child { padding-top: 0 !important; }

/* ── Dark page background ── */
.stApp, [data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: #0d0d12 !important;
}

/* ── Brand tokens ── */
:root {
    --ct-bg:         #0d0d12;
    --ct-surface:    #111118;
    --ct-border:     #1e1e2e;
    --ct-border2:    #2a2a3e;
    --ct-pink:       #e879a0;
    --ct-pink-dim:   #2a0a1a;
    --ct-violet:     #a78bfa;
    --ct-violet-dim: #0f0a1e;
    --ct-amber:      #d97706;
    --ct-amber-dim:  #1a1000;
    --ct-green:      #34d399;
    --ct-green-dim:  #071811;
    --ct-blue:       #60a5fa;
    --ct-blue-dim:   #0a0f1e;
    --ct-text:       #e8e8f0;
    --ct-muted:      #6b6b80;
    --ct-subtle:     #4a4a5a;
    --ct-faint:      #1a1a28;
}

/* ── Navbar shell ── */
.ct-navbar-shell {
    margin: 10px 0 0;
}

.ct-navbar {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
    padding: 16px 20px;
    border: 1px solid rgba(248, 242, 231, 0.09);
    border-radius: 24px;
    background:
        radial-gradient(circle at top right, rgba(168, 139, 250, 0.16), transparent 28%),
        radial-gradient(circle at left center, rgba(96, 165, 250, 0.08), transparent 22%),
        linear-gradient(180deg, rgba(17, 17, 24, 0.98), rgba(15, 16, 24, 0.96));
    box-shadow: 0 18px 42px rgba(0, 0, 0, 0.22);
}

.ct-navbar-mainline {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
}

.ct-brand-block {
    display: flex;
    flex-direction: column;
    gap: 4px;
    align-items: center;
    text-align: center;
    min-width: 0;
}

.ct-logo {
    font-size: 1.12rem;
    font-weight: 800;
    color: #fff;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    white-space: nowrap;
    flex-shrink: 0;
    letter-spacing: -0.03em;
}

.ct-brand-sub {
    color: #a7abc1;
    font-size: 0.78rem;
    margin-top: 0;
    max-width: 34rem;
}

.ct-logo-dot {
    width: 10px; height: 10px;
    border-radius: 50%;
    background: var(--ct-pink);
    display: inline-block;
    flex-shrink: 0;
    box-shadow: 0 0 0 6px rgba(232, 121, 160, 0.12);
}

.ct-credit-cluster {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    gap: 10px;
    flex-wrap: wrap;
}

.ct-credit-label {
    color: #9ca0b8;
    font-size: 0.75rem;
    line-height: 1.4;
}

.ct-credit-link {
    color: #7fcff8;
    text-decoration: none;
    font-weight: 800;
}

.ct-credit-link:hover {
    text-decoration: underline;
}

.ct-tako-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    text-decoration: none;
    padding: 0.48rem 0.78rem;
    border-radius: 999px;
    background: rgba(255, 66, 77, 0.1);
    color: #fff;
    font-size: 0.76rem;
    font-weight: 800;
    border: 1px solid rgba(255, 66, 77, 0.18);
}

.ct-tako-btn:hover {
    background: rgba(255, 66, 77, 0.18);
}

.ct-nav-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.01em;
    background: rgba(232, 121, 160, 0.12);
    color: var(--ct-pink);
    padding: 0.46rem 0.78rem;
    border-radius: 99px;
    border: 1px solid rgba(232, 121, 160, 0.18);
    white-space: nowrap;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) {
    position: sticky;
    top: 10px;
    z-index: 1000;
    max-width: 940px;
    margin: 8px auto 10px !important;
    padding: 7px !important;
    border: 1px solid rgba(248, 242, 231, 0.08);
    border-radius: 20px;
    background:
        linear-gradient(180deg, rgba(20, 21, 31, 0.94), rgba(15, 16, 24, 0.92));
    backdrop-filter: blur(14px);
    box-shadow: 0 16px 34px rgba(0, 0, 0, 0.18);
}

div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px !important;
}

div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div > div {
    min-width: 0;
    flex: 0 1 188px;
    max-width: 220px;
}

/* ── Nav buttons (Streamlit buttons styled as nav links) ── */
.ct-navbtn button {
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.035), rgba(255, 255, 255, 0.015)) !important;
    border: 1px solid rgba(248, 242, 231, 0.06) !important;
    border-radius: 16px !important;
    color: #a6abc2 !important;
    font-size: 0.92rem !important;
    font-weight: 750 !important;
    padding: 0 12px !important;
    height: 44px !important;
    cursor: pointer !important;
    transition: color 0.15s, border-color 0.15s, background 0.15s, transform 0.15s, box-shadow 0.15s !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.02) !important;
    white-space: nowrap !important;
    width: 100% !important;
}
.ct-navbtn button:hover {
    color: #ffffff !important;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.03)) !important;
    border-color: rgba(99, 230, 216, 0.12) !important;
    transform: translateY(-1px);
    box-shadow: 0 10px 18px rgba(0, 0, 0, 0.12) !important;
}
.ct-navbtn-active button {
    color: #ffffff !important;
    border-color: rgba(99, 230, 216, 0.22) !important;
    background:
        radial-gradient(circle at top left, rgba(243, 91, 147, 0.14), transparent 40%),
        linear-gradient(180deg, rgba(99, 230, 216, 0.16), rgba(99, 230, 216, 0.08)) !important;
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.05),
        0 14px 24px rgba(8, 14, 20, 0.22) !important;
}

.ct-navbar-aux {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    max-width: 720px;
    margin: 0 0 10px;
    padding: 10px 14px;
    border: 1px solid rgba(248, 242, 231, 0.06);
    border-radius: 16px;
    background: rgba(255, 255, 255, 0.02);
}

.ct-navbar-aux .ct-credit-cluster {
    gap: 12px;
    justify-content: center;
}

/* ── Content area ── */
.ct-content {
    padding: 26px 4px 36px;
    color: var(--ct-text);
}

/* ── KPI cards ── */
.ct-kpi-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}
@media (max-width: 640px) { .ct-kpi-grid { grid-template-columns: 1fr; } }
@media (max-width: 900px) {
    .ct-navbar-mainline {
        flex-wrap: wrap;
        flex-direction: row;
        align-items: flex-start;
        justify-content: space-between;
    }

    .ct-brand-block {
        align-items: flex-start;
        text-align: left;
    }

    .ct-brand-sub {
        max-width: none;
    }

    .ct-credit-cluster {
        justify-content: flex-start;
    }

    .ct-navbar-aux {
        justify-content: flex-start;
        max-width: none;
        align-items: flex-start;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) {
        max-width: none;
        margin: 8px 0 14px !important;
        border-radius: 18px;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div {
        justify-content: flex-start;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div > div {
        flex: 1 1 0;
        max-width: none;
    }
}

@media (max-width: 640px) {
    .ct-navbar {
        gap: 10px;
        padding: 12px 14px;
        border-radius: 18px;
    }

    .ct-navbar-mainline {
        gap: 10px;
    }

    .ct-logo {
        font-size: 0.96rem;
        white-space: normal;
    }

    .ct-brand-sub {
        font-size: 0.73rem;
    }

    .ct-nav-badge {
        font-size: 0.7rem;
        padding: 0.38rem 0.66rem;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) {
        top: 8px;
        padding: 5px !important;
        border-radius: 16px;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div > div {
        flex: 1 1 calc(50% - 4px);
        width: calc(50% - 4px) !important;
    }

    .ct-navbtn button {
        min-height: 48px !important;
        height: auto !important;
        padding: 10px 12px !important;
        font-size: 0.86rem !important;
        white-space: normal !important;
        line-height: 1.2 !important;
    }

    .ct-navbar-aux {
        gap: 8px;
        padding: 8px 10px;
    }

    .ct-credit-label {
        font-size: 0.72rem;
    }

    .ct-tako-btn {
        font-size: 0.72rem;
        padding: 0.42rem 0.68rem;
    }
}

@media (max-width: 420px) {
    .ct-navbar-mainline {
        align-items: stretch;
    }

    .ct-nav-badge {
        justify-content: center;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div > div {
        flex-basis: 100%;
        width: 100% !important;
    }
}
.ct-kpi {
    background: var(--ct-surface);
    border: 1px solid var(--ct-border);
    border-radius: 10px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
}
.ct-kpi-bar {
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.ct-kpi-label {
    font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em;
    color: var(--ct-subtle); margin-bottom: 8px;
}
.ct-kpi-value { font-size: 28px; font-weight: 700; line-height: 1; }
.ct-kpi-sub   { font-size: 11px; color: var(--ct-subtle); margin-top: 5px; }

/* ── Panel ── */
.ct-panel {
    background: var(--ct-surface);
    border: 1px solid var(--ct-border);
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 12px;
}
.ct-panel-label {
    font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.09em;
    color: var(--ct-subtle); margin-bottom: 12px;
}

/* ── Bar rows ── */
.ct-bar-row { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.ct-bar-name  { font-size: 12px; color: var(--ct-muted); width: 76px; flex-shrink: 0; }
.ct-bar-track { flex: 1; height: 5px; background: var(--ct-faint); border-radius: 99px; overflow: hidden; }
.ct-bar-fill  { height: 100%; border-radius: 99px; }
.ct-bar-count { font-size: 11px; color: var(--ct-subtle); width: 24px; text-align: right; flex-shrink: 0; }

/* ── Feed items ── */
.ct-feed-item {
    display: flex; align-items: center; gap: 10px;
    padding: 8px 0;
    border-bottom: 1px solid var(--ct-faint);
}
.ct-feed-item:last-child { border: none; }
.ct-feed-name  { font-size: 13px; font-weight: 600; color: #d0d0e0; }
.ct-feed-event { font-size: 11px; color: var(--ct-subtle); }
.ct-feed-date  { font-size: 11px; color: var(--ct-subtle); margin-left: auto; white-space: nowrap; }

/* ── Tags / pills ── */
.ct-tag {
    display: inline-block;
    font-size: 10px; font-weight: 700;
    padding: 3px 8px; border-radius: 99px;
    white-space: nowrap;
}
.ct-tag-roulette   { background: var(--ct-pink-dim);   color: var(--ct-pink);   border: 1px solid #2e1228; }
.ct-tag-birthday   { background: var(--ct-amber-dim);  color: var(--ct-amber);  border: 1px solid #2a2000; }
.ct-tag-graduation { background: var(--ct-violet-dim); color: var(--ct-violet); border: 1px solid #1e1430; }
.ct-tag-completed  { background: var(--ct-green-dim);  color: var(--ct-green);  border: 1px solid #0f2820; }
.ct-waiting-pill {
    display: inline-flex; align-items: center; gap: 5px;
    font-size: 11px; font-weight: 600;
    background: var(--ct-amber-dim); color: var(--ct-amber);
    border: 1px solid #2a2000;
    padding: 4px 10px; border-radius: 99px;
}

/* ── Team badges ── */
.ct-team-love      { background: #200010; color: #f43f5e; border: 1px solid #3a0020; }
.ct-team-dream     { background: var(--ct-blue-dim);   color: var(--ct-blue);   border: 1px solid #101828; }
.ct-team-passion   { background: var(--ct-green-dim);  color: var(--ct-green);  border: 1px solid #0f2820; }
.ct-team-trainee   { background: #1a1a28; color: #8080a0; border: 1px solid var(--ct-border2); }
.ct-team-graduated { background: var(--ct-violet-dim); color: var(--ct-violet); border: 1px solid #1e1430; }
.ct-gen-badge {
    font-size: 10px; font-weight: 700;
    padding: 3px 9px; border-radius: 5px;
    background: var(--ct-faint); color: var(--ct-muted);
    border: 1px solid var(--ct-border2);
}

/* ── Timeline cards ── */
.ct-tl-month {
    font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.1em;
    color: var(--ct-subtle); margin: 16px 0 8px;
}
.ct-tl-card {
    display: flex;
    background: var(--ct-surface);
    border: 1px solid var(--ct-border);
    border-radius: 10px;
    overflow: hidden;
    margin-bottom: 8px;
    transition: border-color 0.15s;
}
.ct-tl-card:hover { border-color: var(--ct-border2); }
.ct-tl-banner {
    width: 110px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px; background: #16101e;
    aspect-ratio: 4/3;
}
.ct-tl-banner img { width: 100%; height: 100%; object-fit: cover; display: block; }
.ct-tl-content { flex: 1; padding: 12px 14px; min-width: 0; }
.ct-tl-top {
    display: flex; align-items: flex-start;
    justify-content: space-between; gap: 8px; margin-bottom: 3px;
}
.ct-tl-title { font-size: 14px; font-weight: 600; color: #e0e0f0; }
.ct-tl-time  { font-size: 11px; color: var(--ct-subtle); margin-bottom: 8px; }
.ct-tl-member { display: flex; align-items: center; gap: 8px; }
.ct-member-dot {
    width: 26px; height: 26px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 700; flex-shrink: 0;
}

/* ── Member profile ── */
.ct-member-header {
    display: flex; align-items: flex-start; gap: 16px;
    background: var(--ct-surface);
    border: 1px solid var(--ct-border);
    border-radius: 10px; padding: 20px; margin-bottom: 12px;
}
.ct-member-ava {
    width: 80px; height: 80px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; font-weight: 700; flex-shrink: 0;
    border: 2px solid var(--ct-border2);
    overflow: hidden;
}
.ct-member-ava img { width: 100%; height: 100%; object-fit: cover; }
.ct-member-name { font-size: 18px; font-weight: 700; color: #f0f0f8; line-height: 1.2; margin-bottom: 3px; }
.ct-member-nick { font-size: 13px; color: var(--ct-subtle); margin-bottom: 10px; }
.ct-badge-row   { display: flex; gap: 6px; flex-wrap: wrap; }

.ct-stat-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 10px; margin-bottom: 12px;
}
@media (max-width: 500px) { .ct-stat-grid { grid-template-columns: repeat(2, 1fr); } }
.ct-stat-card {
    background: var(--ct-surface);
    border: 1px solid var(--ct-border);
    border-radius: 10px; padding: 14px; text-align: center;
}
.ct-stat-val   { font-size: 22px; font-weight: 700; line-height: 1; margin-bottom: 3px; }
.ct-stat-label { font-size: 10px; text-transform: uppercase; letter-spacing: 0.07em; color: var(--ct-subtle); }

.ct-history-row {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 0; border-bottom: 1px solid var(--ct-faint);
}
.ct-history-row:last-child { border: none; }
.ct-history-icon {
    width: 46px; height: 35px; border-radius: 6px;
    background: #16101e;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0; overflow: hidden;
}
.ct-history-icon img { width: 100%; height: 100%; object-fit: cover; }
.ct-history-evt  { font-size: 13px; font-weight: 600; color: #d0d0e0; }
.ct-history-date { font-size: 11px; color: var(--ct-subtle); }

/* ── Override Streamlit form inputs to dark ── */
.stTextInput input, .stPasswordInput input,
[data-baseweb="input"] input, [data-baseweb="textarea"] textarea {
    background: var(--ct-surface) !important;
    border-color: var(--ct-border) !important;
    color: var(--ct-text) !important;
}
[data-baseweb="select"] > div {
    background: var(--ct-surface) !important;
    border-color: var(--ct-border) !important;
    color: var(--ct-text) !important;
}
.stDateInput input, .stTimeInput input {
    background: var(--ct-surface) !important;
    color: var(--ct-text) !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: var(--ct-surface) !important;
    border-bottom-color: var(--ct-border) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--ct-muted) !important;
}
.stTabs [aria-selected="true"] {
    color: #fff !important;
    border-bottom-color: var(--ct-pink) !important;
}
</style>
"""

# Backward-compatible public export used by app and page modules.
DARK_THEME_CSS = DARK_CSS

ARCHIVE_THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@600;700;800&family=IBM+Plex+Mono:wght@500;600&family=Manrope:wght@400;500;700;800&display=swap');

:root {
    --ckt-stage: #0b1020;
    --ckt-stage-2: #11172a;
    --ckt-ink: #161a2c;
    --ckt-paper: #f8f2e7;
    --ckt-paper-2: #efe4d1;
    --ckt-pink: #f35b93;
    --ckt-cyan: #63e6d8;
    --ckt-amber: #f6b44b;
    --ckt-lilac: #b8b4d9;
    --ckt-text: #f9f6f0;
    --ckt-muted: rgba(249, 246, 240, 0.66);
    --ckt-line: rgba(248, 242, 231, 0.14);
}

.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background:
        radial-gradient(circle at 10% -10%, rgba(99, 230, 216, 0.14), transparent 28rem),
        radial-gradient(circle at 100% 0%, rgba(243, 91, 147, 0.16), transparent 28rem),
        linear-gradient(140deg, var(--ckt-stage), var(--ckt-stage-2) 58%, #0e1020) !important;
    color: var(--ckt-text);
}

.ct-content.ct-archive {
    padding: 34px 6px 48px;
    font-family: 'Manrope', sans-serif;
}

.ckt-hero {
    display: grid;
    grid-template-columns: minmax(0, 1.18fr) minmax(260px, 0.82fr);
    gap: 18px;
    align-items: start;
    margin-bottom: 18px;
}

.ckt-kicker,
.ckt-meta {
    font: 700 0.73rem/1.4 'IBM Plex Mono', monospace;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--ckt-cyan);
}

.ckt-headline {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-size: clamp(2.4rem, 5vw, 4.7rem);
    line-height: 0.9;
    letter-spacing: -0.06em;
    color: var(--ckt-text);
    margin: 10px 0 14px;
}

.ckt-body {
    color: var(--ckt-muted);
    font-size: 0.98rem;
    line-height: 1.65;
    max-width: 44rem;
}

.ckt-surface {
    background: rgba(22, 26, 44, 0.72);
    border: 1px solid var(--ckt-line);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.24);
}

.ckt-roulette-desk {
    background: linear-gradient(160deg, var(--ckt-paper), var(--ckt-paper-2));
    color: #151220;
    border-radius: 30px 30px 30px 10px;
    padding: 14px;
    transform: rotate(-0.8deg);
    position: relative;
    min-height: 100%;
}

.ckt-roulette-desk:before {
    content: "";
    position: absolute;
    inset: 10px;
    border: 1px dashed rgba(22, 26, 44, 0.24);
    border-radius: 22px;
    pointer-events: none;
}

.ckt-desk-title {
    font: 800 1.55rem/0.95 'Bricolage Grotesque', sans-serif;
    letter-spacing: -0.05em;
    margin: 0 0 8px;
}

.ckt-ticket {
    background: rgba(255, 255, 255, 0.64);
    border-radius: 18px;
    padding: 10px 12px;
    position: relative;
    margin-top: 8px;
}

.ckt-ticket strong {
    display: block;
    margin-top: 4px;
    font-size: 0.98rem;
}

.ckt-ticket.is-waiting:after {
    content: "TBD";
    position: absolute;
    top: -8px;
    right: 14px;
    padding: 5px 8px;
    border-radius: 999px;
    background: var(--ckt-amber);
    color: #151220;
    font: 700 0.67rem/1 'IBM Plex Mono', monospace;
    transform: rotate(8deg);
}

.ckt-stat-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    margin-bottom: 18px;
}

.ckt-stat-card {
    border-radius: 24px;
    padding: 16px 18px;
}

.ckt-stat-card strong {
    display: block;
    font: 800 2rem/1 'Bricolage Grotesque', sans-serif;
    color: var(--accent, var(--ckt-pink));
    margin: 8px 0 6px;
}

.ckt-pulse-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
    margin-top: 18px;
}

.ckt-pulse-card {
    border-radius: 22px;
    padding: 14px;
    background: rgba(248, 242, 231, 0.04);
    border: 1px solid rgba(248, 242, 231, 0.08);
}

.ckt-pulse-value {
    display: block;
    font: 800 1.55rem/1 'Bricolage Grotesque', sans-serif;
    letter-spacing: -0.04em;
    color: var(--ckt-text);
    margin: 8px 0 6px;
}

.ckt-pulse-date {
    font-size: 1.1rem;
    line-height: 1.15;
}

.ckt-spotlight-panel {
    margin-bottom: 18px;
}

.ckt-rank-list {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
}

.ckt-rank-item {
    display: grid;
    grid-template-columns: 54px 48px minmax(0, 1fr) auto;
    gap: 14px;
    align-items: center;
    padding: 12px 14px;
    border-radius: 18px;
    background: rgba(248, 242, 231, 0.04);
    border: 1px solid rgba(248, 242, 231, 0.08);
}

.ckt-rank-position {
    display: grid;
    place-items: center;
    width: 54px;
    height: 54px;
    border-radius: 16px;
    background: rgba(243, 91, 147, 0.12);
    color: var(--ckt-pink);
    font: 800 1rem/1 'IBM Plex Mono', monospace;
}

.ckt-rank-copy {
    min-width: 0;
}

.ckt-rank-avatar {
    display: inline-flex;
    width: 48px;
    height: 48px;
    border-radius: 16px;
    overflow: hidden;
    align-items: center;
    justify-content: center;
    background: rgba(248, 242, 231, 0.08);
    flex-shrink: 0;
}

.ckt-rank-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.ckt-rank-name {
    font: 800 1.12rem/1 'Bricolage Grotesque', sans-serif;
    letter-spacing: -0.03em;
    color: var(--ckt-text);
    margin-bottom: 5px;
}

.ckt-rank-value {
    color: var(--ckt-text);
    font: 800 1.4rem/1 'Bricolage Grotesque', sans-serif;
}

.ckt-grid-2 {
    display: grid;
    grid-template-columns: minmax(0, 1.2fr) minmax(260px, 0.8fr);
    gap: 16px;
}

.ckt-panel {
    border-radius: 26px;
    padding: 18px;
}

.ckt-panel-title {
    font: 800 1.1rem/1 'Bricolage Grotesque', sans-serif;
    letter-spacing: -0.03em;
    color: var(--ckt-text);
    margin: 10px 0 12px;
}

.ckt-panel-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
}

.ckt-panel-note {
    max-width: 220px;
    color: var(--ckt-muted);
    font-size: 0.78rem;
    line-height: 1.45;
    text-align: right;
}

.ckt-bar-row {
    display: grid;
    grid-template-columns: 90px 1fr 30px;
    gap: 10px;
    align-items: center;
    margin-bottom: 10px;
}

.ckt-bar-name,
.ckt-small {
    color: var(--ckt-muted);
    font-size: 0.78rem;
}

.ckt-bar-track {
    height: 7px;
    border-radius: 999px;
    background: rgba(248, 242, 231, 0.08);
    overflow: hidden;
}

.ckt-bar-fill {
    height: 100%;
    border-radius: 999px;
}

.ckt-activity-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(248, 242, 231, 0.08);
}

.ckt-activity-item:last-child {
    border-bottom: none;
}

.ckt-avatar {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    overflow: hidden;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font: 800 0.75rem/1 'IBM Plex Mono', monospace;
    background: var(--ckt-paper);
    color: #151220;
    flex-shrink: 0;
}

.ckt-avatar img,
.ckt-photocard-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.ckt-activity-name {
    font-weight: 700;
    color: var(--ckt-text);
    font-size: 0.9rem;
}

.ckt-activity-top {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 3px;
}

.ckt-activity-date {
    margin-left: auto;
    white-space: nowrap;
}

.ckt-activity-event {
    color: var(--ckt-muted);
    font-size: 0.78rem;
}

.ckt-chip {
    display: inline-flex;
    align-items: center;
    padding: 0.34rem 0.62rem;
    border-radius: 999px;
    white-space: nowrap;
    font: 700 0.66rem/1 'IBM Plex Mono', monospace;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.ckt-chip-roulette { background: rgba(243, 91, 147, 0.16); color: var(--ckt-pink); }
.ckt-chip-birthday { background: rgba(246, 180, 75, 0.16); color: var(--ckt-amber); }
.ckt-chip-graduation { background: rgba(184, 180, 217, 0.16); color: var(--ckt-lilac); }
.ckt-chip-waiting { background: rgba(246, 180, 75, 0.16); color: var(--ckt-amber); }
.ckt-chip-completed { background: rgba(99, 230, 216, 0.16); color: var(--ckt-cyan); }
.ckt-chip-team { background: rgba(248, 242, 231, 0.12); color: var(--ckt-paper); }

.ckt-filter-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 14px;
}

.ckt-filter-copy h1,
.ckt-member-title {
    font: 800 clamp(2rem, 5vw, 3.7rem)/0.93 'Bricolage Grotesque', sans-serif;
    letter-spacing: -0.06em;
    margin: 6px 0 12px;
    color: var(--ckt-text);
}

.ckt-timeline {
    display: grid;
    gap: 10px;
}

.ckt-month-section {
    margin-bottom: 18px;
}

.ckt-timeline-columns {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 16px;
    align-items: start;
}

.ckt-timeline-col {
    min-width: 0;
}

.ckt-month {
    margin-top: 12px;
    color: var(--ckt-cyan);
    font: 700 0.74rem/1.4 'IBM Plex Mono', monospace;
    letter-spacing: 0.14em;
    text-transform: uppercase;
}

.ckt-ticket-card {
    display: grid;
    grid-template-columns: 72px 168px minmax(0, 1fr);
    gap: 14px;
    align-items: stretch;
    border-radius: 28px;
    padding: 12px;
}

.ckt-ticket-card.is-waiting {
    border-color: rgba(246, 180, 75, 0.34);
}

.ckt-date-rail {
    display: grid;
    place-items: center;
    text-align: center;
    border-right: 2px dashed rgba(248, 242, 231, 0.16);
}

.ckt-date-rail strong {
    display: block;
    font: 800 2rem/1 'Bricolage Grotesque', sans-serif;
    color: var(--ckt-paper);
}

.ckt-date-rail span {
    color: var(--ckt-muted);
    font: 700 0.7rem/1 'IBM Plex Mono', monospace;
    text-transform: uppercase;
}

.ckt-banner {
    aspect-ratio: 4 / 3;
    width: 100%;
    min-height: 126px;
    border-radius: 20px;
    background: #0e1020;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(248, 242, 231, 0.56);
    font: 700 0.74rem/1 'IBM Plex Mono', monospace;
}

.ckt-banner img,
.ckt-album-thumb img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    padding: 14px;
    display: block;
}

.ckt-ticket-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
}

.ckt-ticket-copy {
    min-width: 0;
    flex: 1;
}

.ckt-ticket-name {
    font: 800 1.18rem/1.08 'Bricolage Grotesque', sans-serif;
    letter-spacing: -0.03em;
    color: var(--ckt-text);
    margin: 0 0 5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.ckt-member-line {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
    color: var(--ckt-muted);
    font-size: 0.88rem;
}

.ckt-member-pair {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
    margin-top: 10px;
}

.ckt-member-pill {
    min-width: 0;
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 10px;
    border-radius: 14px;
    background: rgba(248, 242, 231, 0.06);
    color: var(--ckt-text);
}

.ckt-member-pill span:last-child {
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.ckt-member-pill.is-waiting {
    justify-content: center;
}

.ckt-member-stage {
    display: flex;
    align-items: flex-start;
    flex-wrap: nowrap;
    gap: 18px;
    border-radius: 32px;
    padding: 18px;
    margin: 12px 0 16px;
}

.ckt-photocard-frame {
    width: 280px;
    min-width: 280px;
    max-width: 280px;
    flex: 0 0 280px;
}

.ckt-photocard-avatar {
    width: 280px;
    max-width: 100%;
    aspect-ratio: 1;
    border-radius: 22px;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(160deg, var(--ckt-paper), var(--ckt-paper-2));
    color: #151220;
    font: 800 2.6rem/1 'Bricolage Grotesque', sans-serif;
    padding: 12px;
}

.ckt-member-stage .ckt-photocard-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center top;
    transform: scale(1.18);
    transform-origin: center top;
    border-radius: 18px;
}

.ckt-member-stage > div:last-child {
    min-width: 0;
    flex: 1 1 auto;
}

.ckt-member-stage .ckt-member-title {
    font-size: clamp(2.2rem, 4vw, 3.6rem);
    line-height: 0.95;
    overflow-wrap: anywhere;
}

.ckt-member-select {
    margin-bottom: 12px;
}

.ckt-card-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 12px;
    margin-bottom: 18px;
}

.ckt-member-card {
    width: 100%;
    text-align: left;
    background: rgba(22, 26, 44, 0.72);
    border: 1px solid var(--ckt-line);
    border-radius: 20px;
    padding: 12px;
    color: var(--ckt-text);
    box-shadow: 0 18px 40px rgba(0, 0, 0, 0.18);
    transition: border-color 0.15s ease, transform 0.15s ease;
}

.ckt-member-card.is-clickable {
    cursor: pointer;
}

.ckt-member-card:hover {
    border-color: rgba(99, 230, 216, 0.32);
    transform: translateY(-2px);
}

.ckt-member-card.is-clickable:hover {
    border-color: rgba(99, 230, 216, 0.42);
    box-shadow: 0 22px 44px rgba(0, 0, 0, 0.24);
}

.ckt-member-card.is-active {
    border-color: rgba(243, 91, 147, 0.5);
    background: rgba(30, 35, 58, 0.95);
}

.ckt-member-browser-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 18px;
}

.ckt-member-browser-item {
    position: relative;
}

.ckt-member-card-link {
    display: block;
    color: inherit;
    text-decoration: none;
}

.ckt-member-modal-toggle {
    position: absolute;
    opacity: 0;
    pointer-events: none;
}

.ckt-member-modal {
    position: fixed;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 32px 20px;
    z-index: 1200;
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
}

.ckt-member-modal-toggle:checked ~ .ckt-member-modal {
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
}

.ckt-member-modal-backdrop {
    position: absolute;
    inset: 0;
    background: rgba(8, 10, 18, 0.74);
    backdrop-filter: blur(8px);
}

.ckt-member-modal-card {
    position: relative;
    width: min(980px, calc(100vw - 40px));
    max-height: min(calc(100vh - 48px), calc(100dvh - 48px));
    overflow: auto;
    border-radius: 30px;
    padding: 18px;
    background: #0b0d16;
    border: 1px solid rgba(248, 242, 231, 0.1);
    box-shadow: 0 28px 80px rgba(0, 0, 0, 0.42);
    overscroll-behavior: contain;
}

.ckt-member-modal-close {
    position: sticky;
    top: 0;
    margin-left: auto;
    display: grid;
    place-items: center;
    width: 34px;
    height: 34px;
    border-radius: 999px;
    text-decoration: none;
    color: var(--ckt-text);
    background: rgba(248, 242, 231, 0.08);
    border: 1px solid rgba(248, 242, 231, 0.12);
    z-index: 2;
    cursor: pointer;
}

.ckt-dialog-section-title {
    color: var(--ckt-text);
    font: 800 0.98rem/1 'Bricolage Grotesque', sans-serif;
    letter-spacing: -0.03em;
    margin: 2px 0 10px;
}

.ckt-member-card-ava {
    width: 100%;
    aspect-ratio: 1;
    border-radius: 16px;
    overflow: hidden;
    background: #fff8ef;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #151220;
    font: 800 1.6rem/1 'Bricolage Grotesque', sans-serif;
    margin-bottom: 10px;
}

.ckt-member-card-ava img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.ckt-member-card-name {
    font: 800 0.95rem/1.1 'Bricolage Grotesque', sans-serif;
    letter-spacing: -0.03em;
    color: var(--ckt-text);
    margin-bottom: 3px;
}

.ckt-member-card-sub {
    color: var(--ckt-muted);
    font-size: 0.76rem;
}

.ckt-meta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 10px 0 14px;
}

.ckt-preset-summary {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 220px;
    gap: 16px;
    align-items: start;
    margin-bottom: 16px;
}

.ckt-preset-copy {
    min-width: 0;
}

.ckt-preset-thumb {
    aspect-ratio: 16 / 9;
    border-radius: 18px;
    overflow: hidden;
    background: #0e1020;
    margin-top: 10px;
}

.ckt-preset-thumb img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    padding: 10px;
    display: block;
}

.ckt-album-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
    gap: 14px;
}

.ckt-album-card {
    border-radius: 22px;
    padding: 10px;
}

.ckt-album-thumb {
    aspect-ratio: 4 / 3;
    border-radius: 16px;
    overflow: hidden;
    background: #0e1020;
    margin-bottom: 10px;
}

.ckt-empty {
    border: 1px dashed rgba(248, 242, 231, 0.18);
    border-radius: 22px;
    padding: 16px;
    color: var(--ckt-muted);
}

@media (max-width: 860px) {
    .ckt-hero,
    .ckt-grid-2,
    .ckt-preset-summary,
    .ckt-ticket-card {
        grid-template-columns: 1fr;
    }

    .ckt-stat-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .ckt-panel-head {
        flex-direction: column;
    }

    .ckt-panel-note {
        max-width: none;
        text-align: left;
    }

    .ckt-date-rail {
        border-right: 0;
        border-bottom: 2px dashed rgba(248, 242, 231, 0.16);
        padding-bottom: 12px;
    }

    .ckt-roulette-desk {
        transform: none;
    }
}

@media (max-width: 1100px) {
    .ckt-member-browser-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
    }
}

@media (max-width: 860px) {
    .ckt-member-browser-grid,
    .ckt-timeline-columns,
    .ckt-member-pair,
    .ckt-album-grid,
    .ckt-pulse-grid,
    .ckt-rank-list,
    .ckt-stat-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .ckt-timeline-columns {
        gap: 12px;
    }

    .ckt-member-stage {
        display: grid;
        grid-template-columns: minmax(0, 220px) minmax(0, 1fr);
        align-items: start;
    }

    .ckt-photocard-frame {
        width: 100%;
        min-width: 0;
        max-width: none;
        flex: 0 0 auto;
    }

    .ckt-photocard-avatar {
        width: 100%;
    }
}

@media (max-width: 640px) {
    .ct-content.ct-archive {
        padding: 24px 0 40px;
    }

    .ckt-member-browser-grid,
    .ckt-timeline-columns,
    .ckt-member-pair,
    .ckt-album-grid,
    .ckt-pulse-grid,
    .ckt-rank-list,
    .ckt-stat-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .ckt-member-browser-grid,
    .ckt-timeline-columns,
    .ckt-album-grid {
        gap: 10px;
    }

    .ckt-member-card {
        border-radius: 18px;
        padding: 10px;
    }

    .ckt-member-card-name {
        font-size: 0.88rem;
    }

    .ckt-member-card-sub {
        font-size: 0.72rem;
    }

    .ckt-ticket-card {
        gap: 12px;
        border-radius: 24px;
        padding: 10px;
    }

    .ckt-banner {
        min-height: 104px;
        border-radius: 16px;
    }

    .ckt-ticket-name {
        font-size: 1rem;
        white-space: normal;
        overflow: visible;
        text-overflow: clip;
    }

    .ckt-member-pill {
        padding: 8px;
    }

    .ckt-member-pill span:last-child {
        font-size: 0.78rem;
    }

    .ckt-member-modal {
        align-items: flex-end;
        padding: 0;
    }

    .ckt-member-modal-card {
        width: 100vw;
        max-height: min(90vh, 90dvh);
        border-radius: 24px 24px 0 0;
        padding: 12px 12px 18px;
        border-left: 0;
        border-right: 0;
        border-bottom: 0;
    }

    .ckt-member-modal-close {
        top: 2px;
        width: 38px;
        height: 38px;
        margin-bottom: 8px;
    }

    .ckt-member-stage {
        grid-template-columns: minmax(0, 112px) minmax(0, 1fr);
        gap: 12px;
        padding: 14px;
        border-radius: 24px;
    }

    .ckt-member-stage .ckt-member-title {
        font-size: clamp(1.55rem, 7vw, 2.1rem);
    }

    .ckt-member-stage .ckt-body {
        font-size: 0.88rem;
    }

    .ckt-meta-row {
        gap: 6px;
        margin: 8px 0 12px;
    }

    .ckt-chip {
        padding: 0.32rem 0.56rem;
        font-size: 0.62rem;
    }
}

@media (max-width: 420px) {
    .ckt-member-browser-grid,
    .ckt-timeline-columns,
    .ckt-member-pair,
    .ckt-album-grid,
    .ckt-pulse-grid,
    .ckt-rank-list,
    .ckt-stat-grid {
        grid-template-columns: 1fr;
    }

    .ckt-member-stage {
        grid-template-columns: 1fr;
    }

    .ckt-photocard-frame {
        max-width: 220px;
        margin: 0 auto;
    }
}
</style>
"""

AVATAR_PALETTES = [
    ("#2a0a1a", "#e879a0"),
    ("#0f0a1e", "#a78bfa"),
    ("#0a0f1e", "#60a5fa"),
    ("#071811", "#34d399"),
    ("#1a1000", "#d97706"),
    ("#200010", "#f43f5e"),
]

TEAM_CLASSES = {
    "LOVE":      "ct-team-love",
    "DREAM":     "ct-team-dream",
    "PASSION":   "ct-team-passion",
    "TRAINEE":   "ct-team-trainee",
    "GRADUATED": "ct-team-graduated",
}

EVENT_EMOJI = {"Roulette": "📸", "Birthday": "🎂", "Graduation": "🎓"}


def apply_styles():
    st.markdown(DARK_CSS, unsafe_allow_html=True)


def render_navbar(active: str, pending: int = 0):
    pages = [
        ("overview", "📊 Overview",      "pages/1_📊_Overview.py"),
        ("timeline", "⏳ Timeline",       "pages/2_⏳_Timeline.py"),
        ("member",   "👤 Member Corner",  "pages/3_👤_Member_Corner.py"),
        ("admin",    "🔐 Admin",          "pages/4_🔐_Admin_Panel.py"),
    ]

    badge_html = (
        f'<span class="ct-nav-badge">{pending} pending</span>'
        if pending > 0 else ""
    )

    st.markdown(f"""
    <div class="ct-navbar-shell">
        <div class="ct-navbar">
            <div class="ct-navbar-mainline">
                <div class="ct-brand-block">
                    <div class="ct-logo">
                        <span class="ct-logo-dot"></span>
                        <span>Chekicha Timeline</span>
                    </div>
                    <div class="ct-brand-sub">Every roulette draw, remembered.</div>
                </div>
                {badge_html}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        cols = st.columns(len(pages), gap="small")

        for i, (key, label, path) in enumerate(pages):
            is_active = (key == active)
            cls = "ct-navbtn ct-navbtn-active" if is_active else "ct-navbtn"
            with cols[i]:
                st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
                if st.button(label, key=f"nav_{key}", use_container_width=True):
                    st.switch_page(path)
                st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="ct-navbar-aux">
        <div class="ct-credit-cluster">
            <span class="ct-credit-label">Developed by <a class="ct-credit-link" href="https://x.com/estrellawin19" target="_blank">@estrellawin19</a></span>
            <a class="ct-tako-btn" href="https://tako.id/Sportagame19Win" target="_blank">Support via Tako</a>
        </div>
    </div>
    """, unsafe_allow_html=True)


def make_tag(event_type: str) -> str:
    cls = {
        "Roulette":   "ct-tag-roulette",
        "Birthday":   "ct-tag-birthday",
        "Graduation": "ct-tag-graduation",
    }.get(event_type, "ct-tag-roulette")
    return f'<span class="ct-tag {cls}">{event_type}</span>'


def make_team_badge(status: str) -> str:
    cls = TEAM_CLASSES.get(status, "ct-gen-badge")
    return f'<span class="ct-tag {cls}">{status}</span>'


def initials_html(name: str, size: int, idx: int = 0) -> str:
    bg, fg = AVATAR_PALETTES[idx % len(AVATAR_PALETTES)]
    initials = "".join(w[0].upper() for w in name.split()[:2]) if name else "?"
    fs = max(10, size // 3)
    return (
        f'<div style="width:{size}px;height:{size}px;border-radius:50%;'
        f'background:{bg};color:{fg};display:flex;align-items:center;'
        f'justify-content:center;font-size:{fs}px;font-weight:700;flex-shrink:0;">'
        f'{initials}</div>'
    )


def safe_text(value) -> str:
    return escape("" if value is None else str(value), quote=True)


def format_event_date(dt) -> str:
    return f"{dt:%a}, {dt.day} {dt:%b %Y}"


def format_event_time(start_dt, end_dt=None) -> str:
    if end_dt is not None:
        return f"{start_dt:%H:%M}-{end_dt:%H:%M} WIB"
    return f"{start_dt:%H:%M} WIB"


def render_event_chip(event_type: str) -> str:
    label = safe_text(event_type or "Roulette")
    slug = "".join(ch for ch in (event_type or "roulette").lower() if ch.isalnum())
    return f'<span class="ckt-chip ckt-chip-{slug}">{label}</span>'


def render_status_chip(is_waiting: bool) -> str:
    if is_waiting:
        return '<span class="ckt-chip ckt-chip-waiting">Waiting for roulette</span>'
    return '<span class="ckt-chip ckt-chip-completed">Completed</span>'


def render_avatar_markup(url: str | None, name: str, class_name: str = "ckt-avatar") -> str:
    if url:
        return f'<span class="{class_name}"><img src="{safe_text(url)}" alt="{safe_text(name)}" loading="lazy"></span>'

    initials = "".join(part[0].upper() for part in (name or "?").split()[:2]) or "?"
    return f'<span class="{class_name}">{safe_text(initials)}</span>'


# Backward-compatible public helpers used by page modules.
tag = make_tag
team_badge = make_team_badge
initials_avatar = initials_html
