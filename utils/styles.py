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
    max-width: 1180px;
    margin: 10px auto 0;
}

.ct-navbar {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
    padding: 14px 18px;
    border: 1px solid rgba(248, 242, 231, 0.1);
    border-radius: 24px;
    background:
        radial-gradient(circle at top right, rgba(255, 106, 139, 0.16), transparent 24%),
        radial-gradient(circle at left center, rgba(120, 224, 209, 0.1), transparent 22%),
        linear-gradient(180deg, rgba(22, 27, 45, 0.985), rgba(16, 20, 34, 0.97));
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.04),
        0 18px 44px rgba(0, 0, 0, 0.2);
}

.ct-navbar-mainline {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
}

.ct-brand-block {
    display: flex;
    flex-direction: column;
    gap: 4px;
    align-items: flex-start;
    text-align: left;
    min-width: 0;
}

.ct-navbar-side {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 10px;
    flex-wrap: wrap;
}

.ct-logo {
    font-size: 1.08rem;
    font-weight: 800;
    color: #fff;
    display: inline-flex;
    align-items: center;
    gap: 9px;
    white-space: nowrap;
    flex-shrink: 0;
    letter-spacing: -0.03em;
}

.ct-brand-sub {
    color: #b2b7ca;
    font-size: 0.76rem;
    margin-top: 0;
    max-width: 34rem;
    line-height: 1.45;
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
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
}

.ct-credit-label {
    color: #9ca0b8;
    font-size: 0.7rem;
    line-height: 1.4;
    letter-spacing: 0.02em;
}

.ct-credit-link {
    color: #7fcff8;
    text-decoration: none;
    font-weight: 800;
}

.ct-credit-link:hover {
    text-decoration: underline;
}

.ct-nav-credit {
    display: inline-flex;
    align-items: center;
    padding: 0.5rem 0.82rem;
    border-radius: 999px;
    background: linear-gradient(180deg, rgba(243, 235, 221, 0.06), rgba(243, 235, 221, 0.03));
    border: 1px solid rgba(243, 235, 221, 0.1);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
}

.ct-tako-btn {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    text-decoration: none;
    padding: 0.5rem 0.9rem;
    border-radius: 999px;
    background: linear-gradient(180deg, rgba(255, 106, 139, 0.12), rgba(255, 106, 139, 0.06));
    color: #ffe7ef;
    font-size: 0.74rem;
    font-weight: 800;
    border: 1px solid rgba(255, 106, 139, 0.22);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

.ct-tako-btn:hover {
    background: linear-gradient(180deg, rgba(255, 106, 139, 0.18), rgba(255, 106, 139, 0.1));
}

div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) {
    position: sticky;
    top: 8px;
    z-index: 1000;
    max-width: 1180px;
    width: 100%;
    margin: 8px auto 8px !important;
    padding: 8px !important;
    border: 1px solid rgba(248, 242, 231, 0.08);
    border-radius: 22px;
    background:
        linear-gradient(180deg, rgba(28, 34, 56, 0.94), rgba(16, 20, 34, 0.92));
    backdrop-filter: blur(14px);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.04),
        0 16px 32px rgba(0, 0, 0, 0.16);
    overflow: visible;
}

div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0 !important;
}

div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div > div {
    position: relative;
    min-width: 0;
    flex: 1 1 0;
    max-width: none;
    padding: 0 2px;
}

div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div > div:not(:last-child):after {
    content: "";
    position: absolute;
    top: 10px;
    right: 0;
    bottom: 10px;
    width: 1px;
    background: linear-gradient(180deg, transparent, rgba(248, 242, 231, 0.12), transparent);
}

/* ── Nav buttons (Streamlit buttons styled as nav links) ── */
.ct-navbtn button {
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.012)) !important;
    border: 1px solid rgba(248, 242, 231, 0.06) !important;
    border-radius: 16px !important;
    color: #a6abc0 !important;
    font-size: 0.88rem !important;
    font-weight: 750 !important;
    padding: 0 14px !important;
    height: 48px !important;
    cursor: pointer !important;
    transition: color 0.15s, border-color 0.15s, background 0.15s, transform 0.15s, box-shadow 0.15s !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.02) !important;
    white-space: nowrap !important;
    width: 100% !important;
    letter-spacing: -0.01em !important;
}

.ct-navbtn button:focus-visible {
    outline: 2px solid rgba(120, 224, 209, 0.8) !important;
    outline-offset: 1px !important;
}

.ct-navbtn button:hover {
    color: #ffffff !important;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.025)) !important;
    border-color: rgba(120, 224, 209, 0.14) !important;
    transform: translateY(-1px);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.03),
        0 10px 18px rgba(5, 10, 20, 0.14) !important;
}
.ct-navbtn-active button {
    color: #ffffff !important;
    border-color: rgba(120, 224, 209, 0.26) !important;
    background:
        radial-gradient(circle at top left, rgba(255, 106, 139, 0.16), transparent 42%),
        linear-gradient(180deg, rgba(120, 224, 209, 0.16), rgba(120, 224, 209, 0.05)) !important;
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.05),
        0 12px 20px rgba(8, 14, 20, 0.18) !important;
}

.ct-navbar-aux {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
    max-width: 1180px;
    margin: 4px auto 8px;
    padding: 0 4px;
    border: 0;
    border-radius: 0;
    background: transparent;
}

.ct-navbar-aux .ct-credit-cluster {
    gap: 8px;
    justify-content: flex-start;
}

.ct-session-stack {
    display: grid;
    gap: 6px;
    justify-items: start;
    width: 100%;
    padding: 10px 12px;
    border-radius: 16px;
    border: 1px solid rgba(243, 235, 221, 0.08);
    background: linear-gradient(180deg, rgba(243, 235, 221, 0.05), rgba(243, 235, 221, 0.02));
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03);
}

.ct-session-stack.is-guest {
    display: flex;
    align-items: center;
    gap: 10px;
    width: auto;
    max-width: 38rem;
    padding: 0;
    border: 0;
    background: transparent;
    box-shadow: none;
}

.ct-session-kicker {
    color: #9ca0b8;
    font-size: 0.72rem;
    line-height: 1.2;
    letter-spacing: 0.02em;
}

.ct-auth-combo-copy {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

.ct-auth-combo-copy .ct-session-note.is-guest {
    color: #b3b8ca;
}

div[data-testid="stHorizontalBlock"]:has(.ct-auth-row) {
    max-width: 1180px;
    width: 100%;
    margin: 0 auto 6px !important;
    padding: 0 !important;
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
}

div[data-testid="stHorizontalBlock"]:has(.ct-auth-row) > div {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px !important;
}

div[data-testid="stHorizontalBlock"]:has(.ct-auth-row) > div > div:first-child {
    flex: 1 1 auto;
    max-width: none;
    min-width: 0;
    padding: 0 !important;
}

div[data-testid="stHorizontalBlock"]:has(.ct-auth-row) > div > div:last-child {
    flex: 0 0 132px;
    max-width: 132px;
    min-width: 132px;
    padding: 0 !important;
}

div[data-testid="stHorizontalBlock"]:has(.ct-auth-row) [data-testid="column"],
div[data-testid="stHorizontalBlock"]:has(.ct-auth-row) .element-container,
div[data-testid="stHorizontalBlock"]:has(.ct-auth-row) .stButton {
    margin: 0 !important;
    padding: 0 !important;
}

.ct-session-note {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    color: #aab0c7;
    font-size: 0.75rem;
    line-height: 1.3;
}

.ct-session-note.is-guest {
    color: #9ca0b8;
    display: inline;
    line-height: 1.35;
}

.ct-session-user {
    color: #eef0f8;
    font-weight: 700;
}

.ct-auth-row {
    display: block;
    width: 100%;
    min-width: 0;
}

.ct-session-role {
    display: inline-flex;
    align-items: center;
    padding: 0.2rem 0.56rem;
    border-radius: 999px;
    background: rgba(120, 224, 209, 0.1);
    border: 1px solid rgba(120, 224, 209, 0.18);
    color: #9af0e5;
    font-size: 0.66rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

div[data-testid="stHorizontalBlock"]:has(.ct-authbtn) {
    max-width: 1180px;
    width: 100%;
    margin: 0 auto 6px !important;
    padding: 0 !important;
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
}

div[data-testid="stHorizontalBlock"]:has(.ct-authbtn) > div {
    display: flex;
    justify-content: flex-end;
    gap: 8px !important;
}

div[data-testid="stHorizontalBlock"]:has(.ct-authbtn) > div > div {
    flex: 0 0 auto;
    width: auto !important;
    max-width: none;
    min-width: 0;
    padding: 0 !important;
}

div[data-testid="stHorizontalBlock"]:has(.ct-authbtn) [data-testid="column"],
div[data-testid="stHorizontalBlock"]:has(.ct-authbtn) .element-container,
div[data-testid="stHorizontalBlock"]:has(.ct-authbtn) .stButton {
    margin: 0 !important;
    padding: 0 !important;
}

.ct-authbtn button {
    width: auto !important;
    min-width: 132px;
    min-height: 42px !important;
    padding: 0 16px !important;
    border-radius: 999px !important;
    border: 1px solid rgba(243, 235, 221, 0.1) !important;
    background: linear-gradient(180deg, rgba(243, 235, 221, 0.06), rgba(243, 235, 221, 0.025)) !important;
    color: #f4f6fb !important;
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.03),
        0 10px 20px rgba(5, 10, 20, 0.12) !important;
}

div[data-testid="stHorizontalBlock"]:has(.ct-auth-combo) {
    max-width: 1180px;
    width: 100%;
    margin: 0 auto 6px !important;
    padding: 10px 12px !important;
    border-radius: 16px;
    border: 1px solid rgba(243, 235, 221, 0.08) !important;
    background: linear-gradient(180deg, rgba(243, 235, 221, 0.05), rgba(243, 235, 221, 0.02)) !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.03) !important;
}

div[data-testid="stHorizontalBlock"]:has(.ct-auth-combo) > div {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px !important;
}

div[data-testid="stHorizontalBlock"]:has(.ct-auth-combo) > div > div:first-child {
    flex: 1 1 auto;
    max-width: none;
    min-width: 0;
    padding: 0 !important;
}

div[data-testid="stHorizontalBlock"]:has(.ct-auth-combo) > div > div:last-child {
    flex: 0 0 auto;
    width: auto !important;
    max-width: none;
    min-width: 180px;
    padding: 0 !important;
}

div[data-testid="stHorizontalBlock"]:has(.ct-auth-combo) [data-testid="column"],
div[data-testid="stHorizontalBlock"]:has(.ct-auth-combo) .element-container,
div[data-testid="stHorizontalBlock"]:has(.ct-auth-combo) .stButton {
    margin: 0 !important;
    padding: 0 !important;
}

.ct-authbtn button:hover {
    background: linear-gradient(180deg, rgba(243, 235, 221, 0.1), rgba(243, 235, 221, 0.04)) !important;
    border-color: rgba(243, 235, 221, 0.14) !important;
}

.ct-authbtn-subtle button {
    background: linear-gradient(180deg, rgba(255, 106, 139, 0.09), rgba(255, 106, 139, 0.04)) !important;
    border-color: rgba(255, 106, 139, 0.18) !important;
    color: #ffdbe4 !important;
}

.ct-authbtn-subtle button:hover {
    background: linear-gradient(180deg, rgba(255, 106, 139, 0.14), rgba(255, 106, 139, 0.06)) !important;
}

.ct-nav-status {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    padding: 9px 12px;
    border-radius: 999px;
    background: linear-gradient(180deg, rgba(243, 235, 221, 0.07), rgba(243, 235, 221, 0.035));
    border: 1px solid rgba(243, 235, 221, 0.12);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
    flex-wrap: wrap;
}

.ct-nav-status-label {
    color: #86ece2;
    font: 700 0.6rem/1.2 'Poppins', sans-serif;
    letter-spacing: 0.03em;
}

.ct-nav-status-value {
    color: #e7e8f3;
    font-size: 0.8rem;
    font-weight: 800;
    letter-spacing: -0.02em;
}

.ct-nav-status-value.is-waiting {
    color: #f197b7;
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
        align-items: flex-start;
        justify-content: space-between;
    }

    .ct-brand-block {
        align-items: flex-start;
        text-align: left;
    }

    .ct-navbar-side {
        width: 100%;
        justify-content: space-between;
    }

    .ct-brand-sub {
        max-width: none;
    }

    .ct-credit-cluster {
        justify-content: flex-start;
    }

    .ct-nav-credit {
        padding: 0.44rem 0.72rem;
    }

    .ct-navbar-aux {
        justify-content: space-between;
        max-width: none;
        align-items: flex-start;
        gap: 6px;
        margin: 2px 0 6px;
        padding: 0 2px;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-authbtn) {
        max-width: none;
        margin: 0 0 8px !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-auth-combo) {
        max-width: none;
        margin: 0 0 8px !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-auth-row) {
        max-width: none;
        margin: 0 0 8px !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-auth-row) > div {
        align-items: flex-start;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-auth-combo) > div {
        align-items: center;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-authbtn) > div {
        justify-content: flex-end;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) {
        max-width: none;
        margin: 6px 0 10px !important;
        padding: 5px !important;
        border-radius: 18px;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div > div:not(:last-child):after {
        display: none;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div {
        justify-content: flex-start;
        gap: 8px !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div > div {
        flex: 1 1 0;
        max-width: none;
        padding: 0;
    }

    .ct-navbtn button {
        background: linear-gradient(180deg, rgba(255, 255, 255, 0.035), rgba(255, 255, 255, 0.015)) !important;
        border: 1px solid rgba(248, 242, 231, 0.06) !important;
        border-radius: 16px !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.02) !important;
    }

    .ct-nav-status {
        justify-items: start;
    }
}

@media (max-width: 640px) {
    .block-container {
        padding-top: 0 !important;
        padding-left: 12px !important;
        padding-right: 12px !important;
    }

    .ct-navbar {
        gap: 8px;
        padding: 11px 12px 11px;
        border-radius: 20px;
    }

    .ct-navbar-mainline {
        gap: 8px;
    }

    .ct-navbar-side {
        justify-content: flex-start;
        gap: 8px;
    }

    .ct-logo {
        font-size: 0.92rem;
        white-space: normal;
    }

    .ct-brand-sub {
        font-size: 0.69rem;
        max-width: none;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) {
        top: 8px;
        padding: 1px !important;
        border-radius: 16px;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div {
        display: flex !important;
        flex-direction: column;
        gap: 0 !important;
    }

div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div > div {
        flex: 1 1 100%;
        width: 100% !important;
        min-width: 0;
        padding: 0 !important;
        height: auto !important;
        min-height: 0 !important;
    }

div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) [data-testid="column"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) [data-testid="column"] > .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }

div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) .stButton {
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) .stButton > button {
        margin: 0 !important;
    }

    .ct-navbtn button {
        min-height: 38px !important;
        height: auto !important;
        padding: 7px 10px !important;
        font-size: 0.82rem !important;
        white-space: normal !important;
        line-height: 1.15 !important;
        margin: 0 !important;
    }

    .ct-navbar-aux {
        align-items: flex-start;
        gap: 5px;
        margin: 2px 0 6px;
        padding: 0 2px;
    }

    .ct-session-note {
        flex-wrap: wrap;
        font-size: 0.71rem;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-authbtn) {
        margin: 0 0 6px !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-auth-combo) {
        margin: 0 0 6px !important;
        padding: 9px 10px !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-auth-row) > div {
        flex-direction: column;
        align-items: stretch;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-auth-combo) > div {
        flex-direction: column;
        align-items: stretch;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-auth-row) > div > div:first-child,
    div[data-testid="stHorizontalBlock"]:has(.ct-auth-row) > div > div:last-child {
        flex: 1 1 auto;
        max-width: none;
        min-width: 0;
        width: 100% !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-authbtn) > div {
        justify-content: flex-start;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-auth-combo) > div > div:first-child,
    div[data-testid="stHorizontalBlock"]:has(.ct-auth-combo) > div > div:last-child {
        width: 100% !important;
        min-width: 0;
    }

    .ct-auth-combo-copy {
        align-items: flex-start;
        gap: 6px;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-authbtn) > div > div {
        flex: 1 1 auto;
        width: 100% !important;
    }

    .ct-authbtn button {
        width: 100% !important;
        min-width: 0;
        min-height: 38px !important;
        font-size: 0.76rem !important;
    }

    .ct-nav-status-label {
        font-size: 0.55rem;
    }

    .ct-nav-status-value {
        font-size: 0.7rem;
    }

    .ct-credit-label {
        font-size: 0.68rem;
    }

    .ct-session-kicker {
        font-size: 0.67rem;
    }

    .ct-tako-btn {
        font-size: 0.68rem;
        padding: 0.36rem 0.6rem;
    }
}

@media (max-width: 420px) {
    .ct-navbar-mainline {
        align-items: stretch;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) {
        padding: 1px !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div {
        gap: 0 !important;
    }

div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div > div {
        width: 100% !important;
        padding: 0 !important;
        height: auto !important;
        min-height: 0 !important;
    }

    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) .element-container,
    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) .stButton,
    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) [data-testid="column"] {
        padding: 0 !important;
        margin: 0 !important;
    }

    .ct-navbtn button {
        min-height: 33px !important;
        padding: 5px 8px !important;
        font-size: 0.78rem !important;
        margin: 0 !important;
    }

    .ct-authbtn button {
        min-height: 32px !important;
        padding: 0 10px !important;
        font-size: 0.74rem !important;
    }
}

@media (max-width: 340px) {
    div[data-testid="stHorizontalBlock"]:has(.ct-navbtn) > div {
        grid-template-columns: 1fr;
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
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

:root {
    --ckt-stage: #14182a;
    --ckt-stage-2: #20263d;
    --ckt-ink: #1b2034;
    --ckt-paper: #f3ebdd;
    --ckt-paper-2: #eadfcd;
    --ckt-pink: #ff6a8b;
    --ckt-cyan: #78e0d1;
    --ckt-amber: #f2b24a;
    --ckt-lilac: #c3bcdd;
    --ckt-text: #faf7f2;
    --ckt-muted: rgba(250, 247, 242, 0.66);
    --ckt-line: rgba(243, 235, 221, 0.12);
}

.stTextInput label,
.stSelectbox label,
.stMultiSelect label,
.stDateInput label,
.stTimeInput label,
.stSegmentedControl label {
    color: var(--ckt-muted) !important;
}

.stTextInput input,
.stPasswordInput input,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-baseweb="select"] > div,
.stDateInput input,
.stTimeInput input {
    border-radius: 14px !important;
    min-height: 44px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    flex-wrap: wrap;
    border-bottom: 0;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 999px;
    min-height: 40px;
    padding: 0 14px;
    border: 1px solid rgba(243, 235, 221, 0.08);
    background: rgba(243, 235, 221, 0.03) !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(120, 224, 209, 0.08) !important;
    border-color: rgba(120, 224, 209, 0.22) !important;
}

div[data-testid="stPopover"] > button,
div[data-testid="stPopover"] button[kind="secondary"] {
    width: 100%;
    min-height: 40px;
    border-radius: 999px !important;
    border: 1px solid rgba(243, 235, 221, 0.1) !important;
    background: rgba(243, 235, 221, 0.04) !important;
    color: #f4f6fb !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    box-shadow: none !important;
}

div[data-testid="stPopover"] > button:hover,
div[data-testid="stPopover"] button[kind="secondary"]:hover {
    background: rgba(243, 235, 221, 0.08) !important;
    border-color: rgba(243, 235, 221, 0.14) !important;
}

div[data-testid="stPopover"] > button:focus-visible,
div[data-testid="stPopover"] button[kind="secondary"]:focus-visible {
    outline: 2px solid rgba(120, 224, 209, 0.8) !important;
    outline-offset: 1px !important;
}

[role="radiogroup"] {
    gap: 8px;
    flex-wrap: wrap;
}

[role="radiogroup"] label {
    border-radius: 999px !important;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
button,
input,
textarea,
select {
    font-family: 'Poppins', sans-serif !important;
}

.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background:
        radial-gradient(circle at 10% -10%, rgba(99, 230, 216, 0.14), transparent 28rem),
        radial-gradient(circle at 100% 0%, rgba(243, 91, 147, 0.16), transparent 28rem),
        linear-gradient(140deg, var(--ckt-stage), var(--ckt-stage-2) 58%, #0e1020) !important;
    color: var(--ckt-text);
}

.ct-content.ct-archive {
    padding: 8px 6px 32px;
    font-family: 'Poppins', sans-serif;
}

.ckt-hero {
    display: grid;
    gap: 12px;
    align-items: start;
    margin-bottom: 12px;
}

.ckt-kicker,
.ckt-meta {
    font: 700 0.76rem/1.4 'Poppins', sans-serif;
    letter-spacing: 0.03em;
    color: var(--ckt-cyan);
}

.ckt-headline {
    font-family: 'Poppins', sans-serif;
    font-size: clamp(2.4rem, 5vw, 4.7rem);
    line-height: 0.96;
    letter-spacing: -0.04em;
    color: var(--ckt-text);
    margin: 4px 0 10px;
}

.ckt-body {
    color: var(--ckt-muted);
    font-size: 1rem;
    line-height: 1.62;
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
    border-radius: 26px;
    padding: 14px;
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
    font: 800 1.55rem/1 'Poppins', sans-serif;
    letter-spacing: -0.03em;
    margin: 0 0 4px;
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
    font: 700 0.67rem/1 'Poppins', sans-serif;
    transform: rotate(8deg);
}

.ckt-stat-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
    margin-top: 12px;
}

.ckt-stat-card {
    border-radius: 20px;
    padding: 14px 15px;
    background: rgba(243, 235, 221, 0.04);
    border: 1px solid rgba(243, 235, 221, 0.08);
}

.ckt-stat-card strong {
    display: block;
    font: 800 1.7rem/0.96 'Poppins', sans-serif;
    font-variant-numeric: tabular-nums;
    color: var(--accent, var(--ckt-pink));
    margin: 6px 0 4px;
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
    font: 800 1.55rem/1 'Poppins', sans-serif;
    font-variant-numeric: tabular-nums;
    letter-spacing: -0.04em;
    color: var(--ckt-text);
    margin: 8px 0 6px;
}

.ckt-pulse-date {
    font-size: 1.1rem;
    line-height: 1.15;
}

.ckt-spotlight-panel {
    margin-bottom: 14px;
}

.ckt-rank-list {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 8px;
}

.ckt-rank-item {
    display: grid;
    grid-template-columns: 42px 40px minmax(0, 1fr) auto;
    gap: 10px;
    align-items: center;
    padding: 10px 12px;
    border-radius: 16px;
    background: rgba(243, 235, 221, 0.04);
    border: 1px solid rgba(243, 235, 221, 0.08);
}

.ckt-rank-position {
    display: grid;
    place-items: center;
    width: 42px;
    height: 42px;
    border-radius: 14px;
    background: rgba(255, 106, 139, 0.12);
    color: var(--ckt-pink);
    font: 800 0.88rem/1 'Poppins', sans-serif;
}

.ckt-rank-copy {
    min-width: 0;
}

.ckt-rank-avatar {
    display: inline-flex;
    width: 40px;
    height: 40px;
    border-radius: 14px;
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
    font: 800 1rem/1.05 'Poppins', sans-serif;
    letter-spacing: -0.025em;
    color: var(--ckt-text);
    margin-bottom: 3px;
}

.ckt-rank-value {
    color: var(--ckt-text);
    font: 800 1.3rem/1 'Poppins', sans-serif;
    font-variant-numeric: tabular-nums;
}

.ckt-grid-2 {
    display: grid;
    grid-template-columns: minmax(0, 1.18fr) minmax(280px, 0.82fr);
    gap: 12px;
}

.ckt-panel {
    border-radius: 24px;
    padding: 15px;
}

.ckt-panel-title {
    font: 800 1.08rem/1.18 'Poppins', sans-serif;
    letter-spacing: -0.02em;
    color: var(--ckt-text);
    margin: 6px 0 10px;
}

.ckt-panel-head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 12px;
}

.ckt-panel-note {
    max-width: 280px;
    color: var(--ckt-muted);
    font-size: 0.82rem;
    line-height: 1.5;
    text-align: left;
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
    padding: 9px 0;
    border-bottom: 1px solid rgba(243, 235, 221, 0.08);
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
    font: 800 0.75rem/1 'Poppins', sans-serif;
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
    font: 700 0.66rem/1 'Poppins', sans-serif;
    letter-spacing: 0.03em;
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
    margin-bottom: 8px;
}

.ckt-compact-intro {
    display: grid;
    gap: 8px;
    margin-bottom: 10px;
}

.ckt-intro-panel {
    border-radius: 22px;
    padding: 14px 16px;
}

.ckt-intro-panel .ckt-body {
    margin: 0;
}

.ckt-mini-strip {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 8px;
    margin-bottom: 10px;
}

.ckt-toolbar-note {
    color: var(--ckt-muted);
    font-size: 0.84rem;
    line-height: 1.55;
    margin: 0 0 8px;
}

.ckt-mini-cell {
    min-width: 0;
    padding: 12px 13px;
    border-radius: 18px;
    background: rgba(243, 235, 221, 0.04);
    border: 1px solid rgba(243, 235, 221, 0.08);
}

.ckt-mini-value {
    display: block;
    margin-top: 5px;
    color: var(--ckt-text);
    font: 800 1.02rem/1.08 'Poppins', sans-serif;
    letter-spacing: -0.02em;
    font-variant-numeric: tabular-nums;
}

.ckt-mini-value.is-hot {
    color: var(--ckt-pink);
}

.ckt-browser-meta {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin: 2px 0 8px;
}

.ckt-browser-meta .ckt-small {
    font-size: 0.82rem;
    line-height: 1.45;
}

.ckt-filter-copy h1,
.ckt-member-title {
    font: 800 clamp(2rem, 5vw, 3.7rem)/0.96 'Poppins', sans-serif;
    letter-spacing: -0.04em;
    margin: 6px 0 12px;
    color: var(--ckt-text);
}

.ckt-timeline {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
}

.ckt-month-section {
    margin-bottom: 12px;
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
    margin: 8px 0 6px;
    color: var(--ckt-cyan);
    font: 700 0.82rem/1.4 'Poppins', sans-serif;
    letter-spacing: 0.03em;
}

.ckt-ticket-card {
    display: grid;
    grid-template-columns: 64px 152px minmax(0, 1fr);
    gap: 12px;
    align-items: stretch;
    border-radius: 24px;
    padding: 11px;
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
    font: 800 2rem/1 'Poppins', sans-serif;
    color: var(--ckt-paper);
}

.ckt-date-rail span {
    color: var(--ckt-muted);
    font: 700 0.7rem/1 'Poppins', sans-serif;
    text-transform: uppercase;
}

.ckt-banner {
    aspect-ratio: 4 / 3;
    width: 100%;
    min-height: 112px;
    border-radius: 18px;
    background: #0e1020;
    overflow: hidden;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(248, 242, 231, 0.56);
    font: 700 0.74rem/1 'Poppins', sans-serif;
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
    flex-wrap: wrap;
    gap: 12px;
}

.ckt-ticket-copy {
    min-width: 0;
    flex: 1;
}

.ckt-ticket-name {
    font: 800 1.05rem/1.12 'Poppins', sans-serif;
    letter-spacing: -0.02em;
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
    min-height: 44px;
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
    gap: 16px;
    border-radius: 28px;
    padding: 16px;
    margin: 10px 0 14px;
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
    font: 800 2.6rem/1 'Poppins', sans-serif;
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
    border-radius: 18px;
    padding: 10px;
    color: var(--ckt-text);
    box-shadow: 0 16px 34px rgba(0, 0, 0, 0.16);
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
    grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
    gap: 10px;
}

.stSegmentedControl,
.stSelectbox,
.stTextInput,
.stNumberInput,
.stDateInput,
.stTimeInput,
.stTabs {
    margin-bottom: 10px;
}

.stButton {
    margin-bottom: 8px;
}

[data-testid="stForm"] {
    border: 1px solid rgba(243, 235, 221, 0.08);
    border-radius: 22px;
    padding: 16px 18px 10px !important;
    background: rgba(243, 235, 221, 0.035);
    margin-top: 8px;
}

[data-testid="stForm"] button[kind="primaryFormSubmit"],
[data-testid="stForm"] button[type="submit"] {
    min-height: 42px;
    border-radius: 16px !important;
}

.ckt-auth-sidecard,
.ckt-auth-formhead {
    min-height: 100%;
}

.ckt-auth-points {
    display: grid;
    gap: 8px;
    margin-top: 12px;
}

.ckt-auth-point {
    padding: 10px 11px;
    border-radius: 16px;
    background: rgba(243, 235, 221, 0.035);
    border: 1px solid rgba(243, 235, 221, 0.08);
}

.ckt-auth-point strong {
    display: block;
    color: var(--ckt-text);
    font-size: 0.9rem;
    margin-bottom: 2px;
}

.ckt-auth-point span {
    color: var(--ckt-muted);
    font-size: 0.8rem;
    line-height: 1.45;
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
    font: 800 0.98rem/1.1 'Poppins', sans-serif;
    letter-spacing: -0.02em;
    margin: 2px 0 10px;
}

.ckt-member-card-ava {
    width: 100%;
    aspect-ratio: 1;
    border-radius: 14px;
    overflow: hidden;
    background: #fff8ef;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #151220;
    font: 800 1.6rem/1 'Poppins', sans-serif;
    margin-bottom: 8px;
}

.ckt-member-card-ava img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.ckt-member-card-name {
    font: 800 0.92rem/1.12 'Poppins', sans-serif;
    letter-spacing: -0.02em;
    color: var(--ckt-text);
    margin-bottom: 3px;
}

.ckt-member-card-sub {
    color: var(--ckt-muted);
    font-size: 0.72rem;
}

.ckt-meta-row {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin: 8px 0 12px;
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

.ckt-overview-hero {
    gap: 14px;
}

.ckt-overview-lead {
    display: flex;
    align-items: stretch;
    justify-content: space-between;
    gap: 20px;
}

.ckt-overview-lead > div:first-child {
    max-width: 43rem;
}

.ckt-overview-title {
    font: 800 clamp(2.2rem, 4.6vw, 4rem)/0.94 'Poppins', sans-serif;
    letter-spacing: -0.04em;
    margin: 6px 0 10px;
    color: var(--ckt-text);
    max-width: 13ch;
}

.ckt-overview-note {
    align-self: end;
    max-width: 22rem;
    padding: 16px 18px;
    border-radius: 22px;
    background:
        linear-gradient(180deg, rgba(243, 235, 221, 0.08), rgba(243, 235, 221, 0.03)),
        linear-gradient(135deg, rgba(255, 106, 139, 0.08), rgba(120, 224, 209, 0.04));
    border: 1px solid rgba(243, 235, 221, 0.1);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
}

.ckt-status-strip {
    position: relative;
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
    padding: 22px 20px;
    border-radius: 28px;
    overflow: hidden;
    background:
        linear-gradient(180deg, rgba(243, 235, 221, 0.09), rgba(243, 235, 221, 0.03)),
        linear-gradient(140deg, rgba(24, 28, 48, 0.98), rgba(18, 22, 37, 0.98));
    border: 1px solid rgba(243, 235, 221, 0.1);
    box-shadow:
        inset 0 1px 0 rgba(255, 255, 255, 0.04),
        0 18px 34px rgba(10, 14, 22, 0.18);
}

.ckt-status-strip:before,
.ckt-status-strip:after {
    content: "";
    position: absolute;
    left: 22px;
    right: 22px;
    height: 8px;
    background: radial-gradient(circle, rgba(243, 235, 221, 0.85) 0 3px, transparent 3.8px) repeat-x;
    background-size: 18px 8px;
    opacity: 0.14;
    pointer-events: none;
}

.ckt-status-strip:before {
    top: -4px;
}

.ckt-status-strip:after {
    bottom: -4px;
}

.ckt-status-cell {
    position: relative;
    min-width: 0;
    padding: 4px 12px 4px 0;
}

.ckt-status-cell:not(:last-child):after {
    content: "";
    position: absolute;
    top: 4px;
    right: 0;
    bottom: 4px;
    width: 1px;
    background: linear-gradient(180deg, transparent, rgba(243, 235, 221, 0.16), transparent);
}

.ckt-status-value {
    display: block;
    margin-top: 8px;
    font: 800 clamp(1.12rem, 2vw, 1.42rem)/1.02 'Poppins', sans-serif;
    letter-spacing: -0.03em;
    font-variant-numeric: tabular-nums;
    color: var(--ckt-text);
}

.ckt-status-value.is-hot {
    color: var(--ckt-pink);
    text-shadow: 0 0 16px rgba(255, 106, 139, 0.16);
}

.ckt-status-subline {
    margin-top: 7px;
    color: var(--ckt-muted);
    font-size: 0.78rem;
    line-height: 1.4;
}

.ckt-summary-panel .ckt-body {
    margin: 0;
}

.ckt-overview-grid {
    margin-bottom: 14px;
}

.ckt-overview-grid .ckt-panel {
    min-width: 0;
}

.ckt-overview-foot {
    align-items: start;
}

.ckt-guide-panel {
    display: grid;
    gap: 10px;
}

.ckt-guide-list {
    display: grid;
    gap: 8px;
    margin: 0;
    padding: 0;
    list-style: none;
}

.ckt-guide-list li {
    padding: 11px 12px;
    border-radius: 16px;
    background: rgba(243, 235, 221, 0.04);
    border: 1px solid rgba(243, 235, 221, 0.08);
    color: var(--ckt-muted);
    font-size: 0.88rem;
    line-height: 1.45;
}

.ckt-guide-list strong {
    display: block;
    margin-bottom: 4px;
    color: var(--ckt-text);
    font-size: 0.92rem;
}

.ckt-overview-note .ckt-body {
    margin: 0;
    max-width: none;
    color: rgba(250, 247, 242, 0.88);
}

.ckt-guide-list span {
    display: block;
    margin-top: 2px;
    color: var(--ckt-pink);
}

.ckt-collection-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 12px;
    margin-top: 8px;
}

.ckt-collection-row-spacer {
    height: 6px;
}

.ckt-collection-card {
    border-radius: 22px;
    padding: 12px;
    background: rgba(243, 235, 221, 0.04);
    overflow: hidden;
    margin-bottom: 2px;
    transition: transform 0.16s ease, border-color 0.16s ease, background 0.16s ease, box-shadow 0.16s ease;
}

.ckt-collection-card:hover {
    transform: translateY(-2px);
    border-color: rgba(243, 235, 221, 0.16);
    background: rgba(243, 235, 221, 0.055);
    box-shadow: 0 18px 36px rgba(0, 0, 0, 0.16);
}

.ckt-collection-card-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 10px;
}

.ckt-collection-copy {
    min-width: 0;
    flex: 1 1 auto;
}

.ckt-collection-identity {
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
    flex: 1 1 auto;
}

.ckt-collection-avatar {
    width: 52px;
    height: 52px;
    border-radius: 16px;
    overflow: hidden;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--ckt-paper);
    color: #151220;
    flex-shrink: 0;
    font: 800 1rem/1 'Poppins', sans-serif;
}

.ckt-collection-avatar img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.ckt-collection-identity-copy {
    min-width: 0;
}

.ckt-collection-event {
    display: block;
    width: 100%;
    font: 800 1.02rem/1.12 'Poppins', sans-serif;
    letter-spacing: -0.02em;
    color: var(--ckt-text);
    margin: 5px 0 0;
    white-space: nowrap !important;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 100%;
}

.ckt-collection-qty {
    color: #ffe5ec;
    font: 800 1.02rem/1 'Poppins', sans-serif;
    letter-spacing: -0.02em;
    white-space: nowrap;
    min-width: 44px;
    justify-content: center;
    display: inline-flex;
    align-items: center;
    padding: 0.34rem 0.56rem;
    border-radius: 999px;
    background: rgba(255, 106, 139, 0.1);
    border: 1px solid rgba(255, 106, 139, 0.16);
}

.ckt-collection-member {
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
}

.ckt-collection-member-name {
    font-weight: 700;
    color: var(--ckt-text);
    font-size: 0.92rem;
    line-height: 1.15;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.ckt-collection-mini-card {
    border-radius: 18px;
    padding: 10px;
    background: rgba(243, 235, 221, 0.035);
    margin-bottom: 10px;
}

.ckt-collection-mini-title {
    font: 800 0.94rem/1.15 'Poppins', sans-serif;
    color: var(--ckt-text);
    margin-top: 5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.ckt-admin-stage {
    --ckt-admin-accent: #8ef0ba;
}

.ckt-admin-hero {
    grid-template-columns: minmax(0, 1.25fr) minmax(260px, 0.75fr);
    align-items: stretch;
}

.ckt-admin-hero-panel {
    background:
        radial-gradient(circle at top left, rgba(142, 240, 186, 0.12), transparent 28%),
        linear-gradient(180deg, rgba(18, 25, 34, 0.96), rgba(12, 17, 24, 0.98));
    border-color: rgba(142, 240, 186, 0.14);
}

.ckt-admin-note {
    padding: 14px 16px;
    border-radius: 22px;
    background: linear-gradient(180deg, rgba(142, 240, 186, 0.08), rgba(142, 240, 186, 0.03));
    border: 1px solid rgba(142, 240, 186, 0.14);
}

.ckt-admin-note code {
    color: #dfffee;
    background: rgba(11, 13, 22, 0.4);
    padding: 0.14rem 0.34rem;
    border-radius: 8px;
}

.ckt-admin-banner {
    margin: 0 0 10px;
    padding: 12px 14px;
    border-radius: 18px;
    background: rgba(65, 159, 112, 0.22);
    border: 1px solid rgba(142, 240, 186, 0.18);
    color: #9bf4c3;
    font-size: 0.9rem;
    font-weight: 700;
}

.ckt-admin-strip .ckt-mini-cell {
    background: rgba(142, 240, 186, 0.05);
    border-color: rgba(142, 240, 186, 0.12);
}

.ckt-admin-tool-head {
    border-color: rgba(142, 240, 186, 0.14);
    background: linear-gradient(180deg, rgba(24, 33, 42, 0.96), rgba(14, 19, 26, 0.98));
}

.ckt-admin-queue-head {
    align-items: stretch;
}

.ckt-admin-queue-copy {
    min-width: 0;
    flex: 1 1 auto;
}

.ckt-admin-queue-card {
    padding: 12px;
}

.ckt-admin-queue-card .ckt-panel-title {
    margin: 4px 0 6px;
}

.ckt-admin-queue-thumb {
    width: 88px;
    min-width: 88px;
    max-width: 88px;
    aspect-ratio: 4 / 3;
    border-radius: 12px;
    overflow: hidden;
    background: rgba(8, 11, 17, 0.94);
    display: flex;
    align-items: center;
    justify-content: center;
}

.ckt-admin-queue-thumb img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    padding: 6px;
    display: block;
}

.ckt-admin-queue-thumb.is-empty span {
    color: rgba(250, 247, 242, 0.55);
    font-size: 0.72rem;
    font-weight: 600;
}

.ckt-admin-queue-label {
    color: var(--ckt-muted);
    font-size: 0.72rem;
    font-weight: 600;
    margin: 0 0 5px;
}

.ckt-admin-stage .ckt-panel,
.ckt-admin-stage .ckt-surface {
    background: linear-gradient(180deg, rgba(15, 20, 28, 0.94), rgba(10, 14, 20, 0.98));
    border-color: rgba(142, 240, 186, 0.09);
    box-shadow: 0 22px 56px rgba(0, 0, 0, 0.28);
}

.ckt-admin-stage .ckt-kicker,
.ckt-admin-stage .ckt-meta {
    color: #8ef0ba;
}

.ckt-admin-stage .stTextInput input,
.ckt-admin-stage .stPasswordInput input,
.ckt-admin-stage [data-baseweb="input"] input,
.ckt-admin-stage [data-baseweb="textarea"] textarea,
.ckt-admin-stage [data-baseweb="select"] > div,
.ckt-admin-stage .stDateInput input,
.ckt-admin-stage .stTimeInput input {
    background: rgba(8, 11, 17, 0.94) !important;
    border-color: rgba(142, 240, 186, 0.12) !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.02);
}

.ckt-admin-stage .stButton > button,
.ckt-admin-stage button[kind="primaryFormSubmit"] {
    border: 1px solid rgba(142, 240, 186, 0.18) !important;
    background: linear-gradient(180deg, rgba(142, 240, 186, 0.16), rgba(142, 240, 186, 0.08)) !important;
    color: #f3fff8 !important;
    font-weight: 700 !important;
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04), 0 12px 24px rgba(10, 18, 14, 0.18) !important;
}

.ckt-admin-stage .stButton > button:hover,
.ckt-admin-stage button[kind="primaryFormSubmit"]:hover {
    background: linear-gradient(180deg, rgba(142, 240, 186, 0.2), rgba(142, 240, 186, 0.1)) !important;
    border-color: rgba(142, 240, 186, 0.24) !important;
}

.ckt-admin-stage .stCheckbox {
    padding: 4px 0;
}

.ckt-admin-stage .stSuccess {
    background: rgba(65, 159, 112, 0.2) !important;
    border: 1px solid rgba(142, 240, 186, 0.16) !important;
}

.ckt-admin-stage .stInfo {
    background: rgba(115, 186, 255, 0.12) !important;
    border: 1px solid rgba(115, 186, 255, 0.14) !important;
}

.ckt-admin-stage .stWarning {
    background: rgba(242, 178, 74, 0.12) !important;
    border: 1px solid rgba(242, 178, 74, 0.16) !important;
}

.ckt-admin-stage .stError {
    background: rgba(255, 106, 139, 0.12) !important;
    border: 1px solid rgba(255, 106, 139, 0.16) !important;
}

.ckt-admin-stage .stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.ckt-admin-stage .stTabs [data-baseweb="tab"] {
    border-color: rgba(142, 240, 186, 0.12);
    background: rgba(142, 240, 186, 0.03) !important;
}

.ckt-admin-stage .stTabs [aria-selected="true"] {
    background: rgba(142, 240, 186, 0.14) !important;
    border-color: rgba(142, 240, 186, 0.24) !important;
}

@media (max-width: 980px) {
    .ckt-grid-2 {
        grid-template-columns: 1fr;
    }

    .ckt-overview-lead {
        align-items: flex-start;
        flex-direction: column;
    }

    .ckt-status-strip {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .ckt-status-cell:nth-child(2):after {
        display: none;
    }

    .ckt-rank-list {
        grid-template-columns: 1fr;
    }

    .ckt-panel-head {
        flex-direction: column;
    }

    .ckt-panel-note {
        max-width: none;
        text-align: left;
    }

    .ckt-admin-hero {
        grid-template-columns: 1fr;
    }

    .ckt-collection-group-head {
        flex-direction: column;
        align-items: flex-start;
        gap: 3px;
    }
}

@media (max-width: 860px) {
    .ckt-hero,
    .ckt-grid-2,
    .ckt-preset-summary,
    .ckt-ticket-card {
        grid-template-columns: 1fr;
    }

    .ckt-status-strip {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .ckt-status-cell:nth-child(2):after {
        display: none;
    }

    .ckt-overview-lead {
        align-items: flex-start;
        flex-direction: column;
    }

    .ckt-mini-strip {
        grid-template-columns: 1fr;
    }

    .ckt-collection-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .ckt-collection-card {
        padding: 12px;
    }

    .ckt-collection-avatar {
        width: 48px;
        height: 48px;
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
        grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
        gap: 14px;
    }
}

@media (max-width: 860px) {
    .ckt-member-browser-grid,
    .ckt-member-pair,
    .ckt-album-grid,
    .ckt-pulse-grid,
    .ckt-rank-list,
    .ckt-stat-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .ckt-timeline {
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
        padding: 18px 0 36px;
    }

    .stTextInput input,
    .stPasswordInput input,
    [data-baseweb="input"] input,
    [data-baseweb="textarea"] textarea,
    [data-baseweb="select"] > div,
    .stDateInput input,
    .stTimeInput input {
        font-size: 16px !important;
    }

    [role="radiogroup"] label,
    .stTabs [data-baseweb="tab"] {
        min-height: 42px !important;
    }

    .ckt-status-strip {
        grid-template-columns: 1fr;
        padding: 14px 12px;
    }

    .ckt-status-cell {
        padding: 0 0 10px;
    }

    .ckt-status-cell:not(:last-child):after {
        top: auto;
        left: 0;
        right: 0;
        bottom: 0;
        width: auto;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(243, 235, 221, 0.16), transparent);
    }

    .ckt-status-cell:nth-child(2):after {
        display: block;
    }

    .ckt-overview-title {
        max-width: none;
    }

    .ckt-overview-note {
        width: 100%;
        padding: 11px 12px;
    }

    .ckt-mini-cell {
        padding: 10px 11px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
    }

    .stTabs [data-baseweb="tab"] {
        min-height: 42px;
        padding: 0 12px;
        font-size: 0.78rem;
    }

    .ckt-member-browser-grid,
    .ckt-member-pair,
    .ckt-album-grid,
    .ckt-pulse-grid,
    .ckt-stat-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
    }

    .ckt-collection-grid {
        grid-template-columns: 1fr !important;
        gap: 9px;
    }

    .ckt-collection-avatar {
        width: 44px;
        height: 44px;
        border-radius: 14px;
    }

    .ckt-rank-list {
        grid-template-columns: 1fr !important;
    }

    .ckt-member-browser-grid,
    .ckt-album-grid {
        gap: 9px;
    }

    .ckt-browser-meta {
        flex-direction: column;
        align-items: flex-start;
        gap: 4px;
    }

    .ckt-timeline {
        gap: 10px;
        grid-template-columns: 1fr !important;
    }

    .ckt-member-card {
        border-radius: 18px;
        padding: 9px;
        box-shadow: 0 12px 26px rgba(0, 0, 0, 0.14);
    }

    .ckt-member-card-ava {
        border-radius: 14px;
        margin-bottom: 8px;
    }

    .ckt-member-card-name {
        font-size: 0.82rem;
        line-height: 1.12;
    }

    .ckt-member-card-sub {
        font-size: 0.68rem;
        line-height: 1.3;
    }

    .ckt-ticket-card {
        gap: 10px;
        border-radius: 22px;
        padding: 9px;
    }

    .ckt-date-rail {
        padding-bottom: 10px;
    }

    .ckt-date-rail strong {
        font-size: 1.65rem;
    }

    .ckt-date-rail span {
        font-size: 0.62rem;
    }

    .ckt-banner {
        min-height: 96px;
        border-radius: 16px;
    }

    .ckt-banner img,
    .ckt-album-thumb img {
        padding: 10px;
    }

    .ckt-ticket-top {
        gap: 8px;
    }

    .ckt-ticket-name {
        font-size: 0.9rem;
        line-height: 1.08;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .ckt-small {
        font-size: 0.7rem;
        line-height: 1.3;
    }

    .ckt-member-line,
    .ckt-member-pair {
        margin-top: 8px;
    }

    .ckt-member-pill {
        gap: 6px;
        min-height: 40px;
        padding: 7px;
        border-radius: 12px;
    }

    .ckt-member-pill .ckt-avatar {
        width: 28px;
        height: 28px;
        font-size: 0.64rem;
    }

    .ckt-member-pill span:last-child {
        font-size: 0.72rem;
        line-height: 1.2;
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

@media (max-width: 480px) {
    .ckt-member-browser-grid,
    .ckt-album-grid,
    .ckt-mini-strip {
        grid-template-columns: 1fr !important;
        gap: 8px;
    }

    .ckt-member-pair {
        grid-template-columns: 1fr !important;
    }

    .ckt-timeline {
        grid-template-columns: 1fr !important;
        gap: 8px;
    }

    .ckt-member-card {
        padding: 8px;
    }

    .ckt-member-card-ava {
        border-radius: 12px;
        margin-bottom: 7px;
    }

    .ckt-member-card-name {
        font-size: 0.78rem;
    }

    .ckt-member-card-sub {
        font-size: 0.64rem;
    }

    .ckt-ticket-card {
        gap: 9px;
        padding: 8px;
    }

    .ckt-banner {
        min-height: 88px;
    }

    .ckt-toolbar-note,
    .ckt-browser-meta .ckt-small,
    .ckt-small {
        font-size: 0.74rem;
        line-height: 1.45;
    }

    .ckt-banner img,
    .ckt-album-thumb img {
        padding: 8px;
    }

    .ckt-date-rail strong {
        font-size: 1.5rem;
    }

    .ckt-date-rail span {
        font-size: 0.58rem;
    }

    .ckt-ticket-name {
        font-size: 0.84rem;
    }

    .ckt-status-value {
        font-size: 0.98rem;
    }

    .ckt-overview-title,
    .ckt-member-title,
    .ckt-filter-copy h1 {
        font-size: clamp(1.7rem, 9vw, 2.1rem);
    }

    .stTabs [data-baseweb="tab"] {
        width: 100%;
        justify-content: center;
    }

    [role="radiogroup"] {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 6px !important;
        align-items: stretch;
    }

    [role="radiogroup"] label {
        flex: 0 1 auto !important;
        min-width: fit-content;
    }

    [role="radiogroup"] > label,
    [role="radiogroup"] > div {
        width: auto !important;
        margin: 0 !important;
    }

    .ckt-member-pill span:last-child {
        font-size: 0.68rem;
    }

    .ckt-member-pill .ckt-avatar {
        width: 25px;
        height: 25px;
        font-size: 0.58rem;
    }

    .ckt-member-pill {
        min-height: 36px;
    }

    .ckt-chip {
        padding: 0.28rem 0.46rem;
        font-size: 0.58rem;
    }
}

@media (max-width: 420px) {
    .ckt-stat-grid {
        grid-template-columns: 1fr !important;
    }

    .ckt-status-strip {
        border-radius: 20px;
    }

    .ckt-panel,
    .ckt-intro-panel {
        padding: 13px;
        border-radius: 20px;
    }
}

@media (max-width: 340px) {
    .ckt-member-browser-grid,
    .ckt-album-grid,
    .ckt-pulse-grid,
    .ckt-rank-list,
    .ckt-stat-grid {
        grid-template-columns: 1fr;
    }

    .ckt-member-pair {
        grid-template-columns: 1fr !important;
    }

    .ckt-timeline {
        grid-template-columns: 1fr !important;
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
    from utils.auth import current_profile, current_username, hydrate_auth_session, is_admin, is_authenticated, sign_out_user

    hydrate_auth_session()

    profile = current_profile()
    authenticated = is_authenticated()
    show_collection = authenticated
    show_admin = is_admin()

    pages = [
        ("overview", "Home",           "pages/1_📊_Overview.py"),
        ("timeline", "Timeline",       "pages/2_⏳_Timeline.py"),
        ("member",   "Members",        "pages/3_👤_Member_Corner.py"),
    ]
    if show_collection:
        pages.append(("collection", "My Collection", "pages/5_🗂️_My_Collection.py"))
    if show_admin:
        pages.append(("admin", "Admin", "pages/4_🔐_Admin_Panel.py"))

    if pending > 0:
        pending_noun = "draw" if pending == 1 else "draws"
        status_value = f'{pending} {pending_noun} still waiting'
        status_class = "ct-nav-status-value is-waiting"
    else:
        status_value = "Nothing waiting now"
        status_class = "ct-nav-status-value"

    status_html = (
        '<div class="ct-nav-status">'
        '<div class="ct-nav-status-label">Open now</div>'
        f'<div class="{status_class}">{status_value}</div>'
        '</div>'
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
                    <div class="ct-brand-sub">See which draws are still open, who has been assigned, and which members appear most often.</div>
                </div>
                <div class="ct-navbar-side">
                    <div class="ct-nav-credit"><span class="ct-credit-label">Built by <a class="ct-credit-link" href="https://x.com/estrellawin19" target="_blank" rel="noopener noreferrer">@estrellawin19</a></span></div>
                    {status_html}
                    <a class="ct-tako-btn" href="https://tako.id/Sportagame19Win" target="_blank" rel="noopener noreferrer">Support via Tako</a>
                </div>
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

    if authenticated or active != "collection":
        cols = st.columns([4.2, 1], gap="small")
        with cols[0]:
            if authenticated:
                st.markdown(
                    f'<div class="ct-auth-row"><div class="ct-session-stack"><div class="ct-session-kicker">Signed in as</div><div class="ct-session-note"><span class="ct-session-user">@{safe_text(current_username() or "collector")}</span><span class="ct-session-role">{safe_text((profile.get("role", "collector") if profile else "collector"))}</span></div></div></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    '<div class="ct-auth-combo"><div class="ct-session-stack is-guest"><div class="ct-auth-combo-copy"><div class="ct-session-kicker">Save your collection</div><div class="ct-session-note is-guest">Sign in to save your collection.</div></div></div></div>',
                    unsafe_allow_html=True,
                )
        with cols[1]:
            if authenticated:
                st.markdown('<div class="ct-authbtn ct-authbtn-subtle">', unsafe_allow_html=True)
                if st.button("Sign out", key=f"signout_{active}", use_container_width=True):
                    sign_out_user()
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="ct-authbtn">', unsafe_allow_html=True)
                if st.button("Open my collection", key=f"guest_collection_{active}", use_container_width=True):
                    st.switch_page("pages/5_🗂️_My_Collection.py")
                st.markdown('</div>', unsafe_allow_html=True)


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
        return '<span class="ckt-chip ckt-chip-waiting">Needs winner</span>'
    return ''


def render_avatar_markup(url: str | None, name: str, class_name: str = "ckt-avatar") -> str:
    if url:
        return f'<span class="{class_name}"><img src="{safe_text(url)}" alt="{safe_text(name)}" loading="lazy"></span>'

    initials = "".join(part[0].upper() for part in (name or "?").split()[:2]) or "?"
    return f'<span class="{class_name}">{safe_text(initials)}</span>'


# Backward-compatible public helpers used by page modules.
tag = make_tag
team_badge = make_team_badge
initials_avatar = initials_html
