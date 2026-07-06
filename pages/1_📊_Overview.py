import streamlit as st

from utils.admin_access import hydrate_admin_access
from utils.overview_data import build_overview_snapshot
from utils.styles import (
    ARCHIVE_THEME_CSS,
    DARK_THEME_CSS,
    render_avatar_markup,
    render_navbar,
    safe_text,
    format_event_date,
)
from utils.supabase_client import get_supabase


def render_stat_grid(stats):
    cards = "".join(
        (
            f'<div class="ckt-stat-card" style="--accent:{color}">'
            f'<div class="ckt-meta">{safe_text(label)}</div>'
            f'<strong>{value}</strong>'
            f'<div class="ckt-small">{safe_text(subcopy)}</div>'
            f"</div>"
        )
        for label, value, subcopy, color in stats
    )
    return f'<div class="ckt-stat-grid">{cards}</div>'


st.set_page_config(
    page_title="Overview - Chekicha Timeline",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(DARK_THEME_CSS + ARCHIVE_THEME_CSS, unsafe_allow_html=True)

supabase = get_supabase()
events_res = supabase.table("chekicha").select(
    "id, event_type, event_name, start_time, slot_mode, member_id_a, member_id_b, "
    "member_a:member_id_a(nickname, avatar_url, generasi), member_b:member_id_b(nickname, avatar_url, generasi)",
    count="exact",
).execute()

event_rows = events_res.data or []
snapshot = build_overview_snapshot(event_rows)
total_pending = snapshot["pending_slots"]
latest_show_event = snapshot["latest_show_event"]
latest_show_event_copy = format_event_date(latest_show_event) if latest_show_event is not None else "No show/event dates yet"

hydrate_admin_access()
render_navbar("overview", total_pending)
st.markdown('<div class="ct-content ct-archive">', unsafe_allow_html=True)

waiting_copy = (
    f"{total_pending} draw{'s' if total_pending != 1 else ''} still waiting"
    if total_pending
    else "No open draws right now"
)
top_member = snapshot["leaderboard"][0] if snapshot["leaderboard"] else None
top_member_name = top_member["nickname"] if top_member else "No ranking yet"
top_member_subcopy = (
    f"{top_member['count']} show/event slot{'s' if top_member['count'] != 1 else ''} so far"
    if top_member
    else "Ranking starts after someone appears in at least two show/event slots"
)

st.markdown(
    """
    <style>
    .ckt-rank-list-scroll {
        display: grid;
        gap: 8px;
        max-height: 420px;
        overflow-y: auto;
        padding-right: 6px;
    }
    .ckt-rank-list-scroll::-webkit-scrollbar {
        width: 8px;
    }
    .ckt-rank-list-scroll::-webkit-scrollbar-thumb {
        background: rgba(243, 235, 221, 0.16);
        border-radius: 999px;
    }
    .ckt-overview-secondary {
        margin-top: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <section class="ckt-hero ckt-overview-hero">
      <div class="ckt-status-strip ckt-surface">
        <div class="ckt-status-cell">
          <div class="ckt-meta">Show / event sessions</div>
          <strong class="ckt-status-value">{snapshot['show_event_sessions']}</strong>
          <div class="ckt-status-subline">Archive rows that feed the homepage ranking.</div>
        </div>
        <div class="ckt-status-cell">
          <div class="ckt-meta">Latest show / event</div>
          <strong class="ckt-status-value">{safe_text(latest_show_event_copy)}</strong>
          <div class="ckt-status-subline">Most recent show/event date saved in the archive.</div>
        </div>
        <div class="ckt-status-cell">
          <div class="ckt-meta">Top ranked member</div>
          <strong class="ckt-status-value">{safe_text(top_member_name)}</strong>
          <div class="ckt-status-subline">{safe_text(top_member_subcopy)}</div>
        </div>
        <div class="ckt-status-cell">
          <div class="ckt-meta">Open draws</div>
          <strong class="ckt-status-value {'is-hot' if total_pending else ''}">{safe_text(waiting_copy)}</strong>
          <div class="ckt-status-subline">Still tracked here, but no longer the main story.</div>
        </div>
      </div>
      <div class="ckt-overview-lead">
        <div>
          <div class="ckt-kicker">JKT48 cheki tracker</div>
          <h1 class="ckt-overview-title">See who shows up most in show/event cheki.</h1>
          <p class="ckt-body">This homepage now starts from archive patterns: a full ranking, the latest five assigned members, and a quick count of special-event sessions.</p>
        </div>
        <div class="ckt-overview-note">
          <div class="ckt-meta">Scope</div>
          <div class="ckt-body">Birthday and Graduation stay in the counts below, but the main ranking and recent list only read from show/event archive rows.</div>
        </div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

stats = [
    ("Show / Event sessions", snapshot["show_event_sessions"], "All non-birthday, non-graduation archive rows", "#FF6A8B"),
    ("Birthday sessions", snapshot["birthday_sessions"], "Special single-member birthday rows", "#F2B24A"),
    ("Graduation sessions", snapshot["graduation_sessions"], "Special graduation archive rows", "#C3BCDD"),
    ("Assigned show/event slots", snapshot["assigned_show_event_slots"], "Filled slots that feed ranking and recent activity", "#78E0D1"),
]

leaderboard_html = "".join(
    f'''
    <div class="ckt-rank-item">
      <div class="ckt-rank-position">#{row.get("rank", index)}</div>
      {render_avatar_markup(row.get("avatar_url"), row["nickname"], class_name="ckt-rank-avatar")}
      <div class="ckt-rank-copy">
        <div class="ckt-rank-name">{safe_text(row["nickname"])}</div>
        <div class="ckt-small">{safe_text(f"Gen {row['generasi']}") if row.get("generasi") else "Generation unknown"}</div>
      </div>
      <div class="ckt-rank-value">{row["count"]}</div>
    </div>
    '''
    for index, row in enumerate(snapshot["leaderboard"], start=1)
)
if not leaderboard_html:
    leaderboard_html = '<div class="ckt-empty">No members with 2+ show/event appearances yet.</div>'

feed_html = ""
for row in snapshot["recent_assignments"]:
    nickname = row.get("nickname", "Unknown member")
    avatar = render_avatar_markup(row.get("avatar_url"), nickname)
    feed_html += f"""
    <div class="ckt-activity-item">
      {avatar}
      <div style="min-width:0;flex:1">
        <div class="ckt-activity-top">
          <div class="ckt-activity-name">{safe_text(nickname)}</div>
          <span class="ckt-small ckt-activity-date">{safe_text(format_event_date(row['start_dt']))}</span>
        </div>
        <div class="ckt-activity-event">{safe_text(row.get('event_name', 'Untitled event'))}</div>
      </div>
    </div>
    """
if not feed_html:
    feed_html = '<div class="ckt-empty">Recent show/event assignments will appear here.</div>'

st.markdown(
    f"""
    <section class="ckt-grid-2 ckt-overview-grid">
      <div class="ckt-surface ckt-panel ckt-spotlight-panel">
        <div class="ckt-panel-head">
          <div>
            <div class="ckt-meta">Show / event ranking</div>
            <h2 class="ckt-panel-title">Members who appear most often</h2>
          </div>
          <div class="ckt-panel-note">Only members with 2+ appearances are shown. Ties keep the same rank number and are ordered by the latest show/event assignment.</div>
        </div>
        <div class="ckt-rank-list-scroll">{leaderboard_html}</div>
      </div>
      <div class="ckt-surface ckt-panel">
        <div class="ckt-panel-head">
          <div>
            <div class="ckt-meta">Recent 6</div>
            <h2 class="ckt-panel-title">Latest six assigned show/event members</h2>
          </div>
          <div class="ckt-panel-note">Both slots from the same event can appear if both were filled.</div>
        </div>
        {feed_html}
      </div>
    </section>
    <section class="ckt-surface ckt-panel ckt-summary-panel">
      <div class="ckt-panel-head">
        <div>
          <div class="ckt-meta">Quick counts</div>
          <h2 class="ckt-panel-title">How the archive is split right now</h2>
        </div>
        <div class="ckt-panel-note">Small numbers only, no extra chart noise.</div>
      </div>
      {render_stat_grid(stats)}
    </section>
    <section class="ckt-surface ckt-panel ckt-overview-secondary">
      <div class="ckt-panel-head">
        <div>
          <div class="ckt-meta">Pending status</div>
          <h2 class="ckt-panel-title">Open draws still in the archive</h2>
        </div>
        <div class="ckt-panel-note">Operational detail kept here as a secondary check.</div>
      </div>
      <p class="ckt-body">{safe_text(waiting_copy)}. Use the admin or timeline pages when you want to resolve unfinished rows.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)



