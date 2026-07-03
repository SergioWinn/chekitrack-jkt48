# ChekiTrack Hybrid Archive Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign Overview, Timeline, and Member Corner to match the approved Hybrid Archive direction while preserving Streamlit usability.

**Architecture:** Keep Streamlit for data fetching and control flow, but move the primary visual hierarchy into shared HTML/CSS helpers. Extend the existing `utils.styles` module with archive-specific styling and small presentational helpers, then update the three user-facing pages to render photocard, ticket, and album layouts.

**Tech Stack:** Python, Streamlit, Supabase, shared CSS via `st.markdown`, `unittest`

---

### Task 1: Add regression coverage for the redesign contract

**Files:**
- Modify: `tests/test_styles.py`
- Create: `tests/test_page_content.py`

- [ ] **Step 1: Write failing tests for archive styling and page content**
- [ ] **Step 2: Run tests to verify they fail**
- [ ] **Step 3: Implement shared styling and page rewrites**
- [ ] **Step 4: Run tests to verify they pass**

### Task 2: Extend shared UI helpers

**Files:**
- Modify: `utils/styles.py`

- [ ] **Step 1: Add archive CSS tokens and component classes**
- [ ] **Step 2: Add safe formatting helpers for dates, chips, and avatars**
- [ ] **Step 3: Keep backward-compatible exports intact**
- [ ] **Step 4: Run tests**

### Task 3: Redesign Overview

**Files:**
- Modify: `pages/1_📊_Overview.py`

- [ ] **Step 1: Replace compact KPI-first layout with hero + roulette desk**
- [ ] **Step 2: Convert stat cards and activity feed into collectible surfaces**
- [ ] **Step 3: Remove Indonesian copy and Windows-incompatible date formatting**
- [ ] **Step 4: Run tests**

### Task 4: Redesign Timeline

**Files:**
- Modify: `pages/2_⏳_Timeline.py`

- [ ] **Step 1: Convert repeated row cards into grouped ticket-rail cards**
- [ ] **Step 2: Add filter header and raw table expander fallback**
- [ ] **Step 3: Strengthen waiting/completed state presentation**
- [ ] **Step 4: Run tests**

### Task 5: Redesign Member Corner

**Files:**
- Modify: `pages/3_👤_Member_Corner.py`

- [ ] **Step 1: Convert profile header into photocard dossier layout**
- [ ] **Step 2: Replace session list with mini event album grid**
- [ ] **Step 3: Remove remaining Indonesian copy and Windows-incompatible dates**
- [ ] **Step 4: Run tests**

### Task 6: Final verification

**Files:**
- Verify: `utils/styles.py`
- Verify: `pages/1_📊_Overview.py`
- Verify: `pages/2_⏳_Timeline.py`
- Verify: `pages/3_👤_Member_Corner.py`
- Verify: `tests/test_styles.py`
- Verify: `tests/test_page_content.py`

- [ ] **Step 1: Run full targeted test suite**
- [ ] **Step 2: Run import smoke checks for shared helpers**
- [ ] **Step 3: Report actual verification evidence**
