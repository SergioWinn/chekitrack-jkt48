# ChekiTrack JKT48 Hybrid Archive Design

Date: 2026-07-03
Product: ChekiTrack JKT48
Scope: Visual redesign for Overview, Timeline, and Member Corner

## Summary

ChekiTrack should move away from the feel of a standard dark analytics dashboard and toward a fandom archive product. The chosen direction is `Hybrid Archive`: a premium collectible base with visible fandom energy. Member portraits and roulette suspense are the primary emotional hooks. Event banners support the experience as collectible artifacts.

The design language splits responsibilities by page:

- Overview: photocard dashboard with a dominant roulette suspense panel
- Timeline: ticket-album chronology with strong waiting/completed states
- Member Corner: premium photocard dossier with a mini event album

## Product Framing

Subject: JKT48 Chekicha history archive

Audience:

- English-speaking JKT48 fans who want to browse event history
- Maintainers/admins who need the product to remain readable and structured

Single job:

- Turn historical Chekicha records into a collectible archive experience without losing operational clarity

## Design Direction

### Chosen Visual Direction

`Hybrid Archive`

- Premium collectible tone as the foundation
- Ticket and sleeve metaphors used where they reinforce chronology and suspense
- Clean enough for dashboard use, but not neutral or generic

### What Must Feel Premium First

- Member portraits
- Roulette suspense / waiting states

Event banners remain important, but are a supporting layer rather than the lead.

### Signature Element

A combination of:

- photocard sleeve framing for member-centric views
- ticket rail cards for event chronology
- a highlighted roulette desk panel for unresolved events

## UX Critique Of Current Layout

### Current Strengths

- Existing custom CSS already improves baseline Streamlit presentation
- Dark theme is coherent across pages
- Timeline is already closer to cards than raw table output
- Navigation is straightforward

### Current Problems

1. The experience still reads as a utility dashboard first.
   - KPI cards and compact panels create an efficient but emotionally flat first impression.

2. The most distinctive product behavior is underplayed.
   - Waiting roulette states are present, but not treated as the main source of tension.

3. The timeline still feels row-based.
   - Even with cards, the visual rhythm is closer to repeated list items than to a real archive chronology.

4. Member Corner is too small and profile-like.
   - The current header is functional, but not collectible or memorable.

5. Some copy and formatting break the English product promise.
   - There are still Indonesian labels and Windows-incompatible date formatting patterns.

## Experience Principles

1. Lead with emotion, then data.
   - Suspense and collectibles first, counts and distributions second.

2. Make artifacts visible.
   - Portraits, banners, and event cards should feel like objects in a collection.

3. Preserve admin clarity.
   - Dense tables can remain available, but as secondary audit/export layers.

4. Use one strong visual risk.
   - Light ticket/photocard surfaces inside a dark app shell.

## Token System

### Color Palette

- Stage navy: `#0B1020`
- Backstage ink: `#161A2C`
- Photo paper: `#F8F2E7`
- Paper shadow: `#EFE4D1`
- Ribbon pink: `#F35B93`
- Roulette cyan: `#63E6D8`
- Ticket amber: `#F6B44B`
- Archive lilac: `#B8B4D9`

### Typography

- Display: `Bricolage Grotesque`
  - Used for hero headlines, member names, key numbers
- Body: `Manrope`
  - Used for interface copy and descriptions
- Utility: `IBM Plex Mono`
  - Used for dates, filters, status chips, and metadata

### Material Language

- Dark atmospheric canvas behind the content
- Bright paper-like cards for featured objects
- Rounded frames with tactile borders
- Minimal shadows used to separate collectible objects from the base layer

## Page 1: Overview

### Job

Present ChekiTrack as a living archive and surface current roulette suspense immediately.

### Layout

- Left hero column:
  - archive title
  - editorial headline
  - short explanation of the product
- Right hero column:
  - `Roulette Desk` panel
  - waiting count
  - recent completed calls shown like inserted ticket slips
- Below hero:
  - three collectible-style stat cards
- Lower row:
  - event type mix panel
  - latest activity panel

### Why This Works

- The user understands the product thesis before seeing charts
- Waiting roulette becomes the real hook
- Stats still exist, but no longer flatten the page into analytics furniture

### Wireframe

```text
+---------------------------------------------------+----------------------+
| JKT48 Chekicha Archive                            | Roulette Desk        |
| Every roulette draw, remembered.                  | waiting count        |
| editorial intro                                   | recent completed     |
+---------------------------------------------------+----------------------+

+-------------------+-------------------+-------------------+
| Events archived   | Members tracked   | Waiting roulette  |
+-------------------+-------------------+-------------------+

+---------------------------------------+-------------------+
| Event type mix                        | Latest activity   |
+---------------------------------------+-------------------+
```

## Page 2: Timeline

### Job

Make the event history feel like a collectible chronology instead of a table.

### Layout

- Top strip:
  - lightweight event type filter
- Main body:
  - month grouping
  - ticket rail cards for each event
- Ticket rail structure:
  - left: date rail
  - middle: 4:3 event banner
  - right: event info, type chip, member state

### Waiting State

Waiting events must feel unresolved and intentionally highlighted.

- amber treatment
- "Waiting for roulette" state chip
- visually distinct from completed events

### Completed State

Completed events should feel settled.

- avatar and member name shown as reveal result
- calmer cyan/completed treatment

### Why This Works

- Time is read as a sequence, not a spreadsheet
- Banners gain narrative weight
- Waiting vs completed becomes emotionally legible

### Secondary Data Layer

The raw dataframe remains useful, but should move into an expander:

- `Raw table`
- audit/export use only

### Wireframe

```text
JULY 2026

+------+------------------+-----------------------------------------+
| 03   | banner 4:3       | Event name                              |
| JUL  |                  | Fri, 3 Jul 2026 · 19:00-20:00 WIB       |
|      |                  | [Roulette] [Waiting for roulette]       |
+------+------------------+-----------------------------------------+

+------+------------------+-----------------------------------------+
| 01   | banner 4:3       | Event name                              |
| JUL  |                  | Tue, 1 Jul 2026 · 18:30-19:30 WIB       |
|      |                  | [Birthday] avatar Gracie [Completed]    |
+------+------------------+-----------------------------------------+
```

## Page 3: Member Corner

### Job

Make each member page feel like a collectible dossier with a visible call history album.

### Layout

- Top control bar:
  - member selector
- Main profile stage:
  - left: large portrait in photocard sleeve frame
  - right: name, nickname, status, generation, completed calls, latest session
- Lower section:
  - session album grid using mini event cards

### Why This Works

- Member identity becomes the page anchor
- Large portrait supports fandom expectations
- History reads as a collectible archive, not a technical list

### Wireframe

```text
+--------------------------------------------------------------+
| Choose member: [ Gracie ]                                    |
+--------------------------------------------------------------+

+-------------------------+------------------------------------+
| large portrait card     | Gracie                             |
| photocard frame         | nickname                           |
|                         | [DREAM] [Gen 11] [12 completed]    |
|                         | Last completed session: 3 Jul 2026 |
+-------------------------+------------------------------------+

Session Album
+-------------------+-------------------+-------------------+
| banner            | banner            | banner            |
| event name        | event name        | event name        |
| date + type       | date + type       | date + type       |
+-------------------+-------------------+-------------------+
```

## Copy And Content Rules

- Product copy must be fully English
- Replace Indonesian labels such as:
  - `Tipe` -> `Event type`
  - `Pilih member` -> `Choose member`
  - `Riwayat sesi` -> `Session history`
  - `Semua tipe event` -> `All event types`
  - `Aktif dan graduated` -> `Active and graduated`
  - `Pemenang belum diumumkan` -> `Winner not announced`

## Technical Guidance

### Streamlit Approach

- Keep Streamlit for structure, data fetching, and controls
- Replace primary visual surfaces with `st.markdown(..., unsafe_allow_html=True)` where hierarchy matters
- Use `st.container()` and nested `st.columns()` for macro layout
- Keep native widgets for filter and admin actions where interaction matters more than styling

### HTML Safety

- Escape user/database-provided strings before inserting into HTML
- Avoid raw interpolation of event names, member names, and URLs without sanitization

### Date Formatting

- Do not use `strftime("%-d")`
- Use Windows-safe formatting like `f"{dt.day} {dt:%b}"`

## Scope Boundaries

This redesign covers:

- visual hierarchy
- card systems
- layout changes
- copy cleanup for the three main user-facing pages

This redesign does not currently cover:

- Admin Panel redesign beyond consistency touch-ups
- database schema changes
- feature changes to event or member workflows

## Recommended Implementation Order

1. Extend shared style layer with new tokens and components
2. Redesign Overview
3. Redesign Timeline
4. Redesign Member Corner
5. Demote raw table views to secondary surfaces where needed
6. Sweep copy and date formatting issues

## Risks

1. Too much decorative styling could reduce clarity.
   - Mitigation: keep one major signature per page and keep metadata disciplined.

2. Ticket/photocard metaphors could become gimmicky.
   - Mitigation: use them only for primary surfaces, not every component.

3. HTML-heavy rendering could become brittle.
   - Mitigation: centralize helper functions and CSS in shared utilities.

## Acceptance Criteria

- Overview feels like an archive landing page, not a KPI dashboard
- Timeline feels chronological and collectible, not table-first
- Member Corner feels portrait-led and premium
- Waiting roulette is visually stronger than completed states
- English copy is consistent across the redesigned pages
- Raw tables, if retained, are secondary rather than primary
