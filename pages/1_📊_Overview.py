import pandas as pd
import streamlit as st

from utils.admin_access import hydrate_admin_access
from utils.styles import (
    ARCHIVE_THEME_CSS,
    DARK_THEME_CSS,
    render_event_chip,
    render_avatar_markup,
    render_navbar,
    safe_text,
    format_event_date,
)
from utils.supabase_client import get_supabase


def relation_to_member(value):
    if isinstance(value, list):
        return value[0] if value else {}
    return value or {}


def single_member_event(event_type: str | None) -> bool:
    return event_type in {"Birthday", "Graduation"}


def collapse_recent_calls(rows, limit: int = 5):
    collapsed = []
    seen_single_member_days = set()

    for row in sorted(rows, key=lambda item: item["start_time"], reverse=True):
        event_type = row.get("event_type")
        dt = pd.to_datetime(row["start_time"])

        if single_member_event(event_type):
            collapse_key = (
                event_type,
                row.get("event_name"),
                row.get("nickname"),
                dt.date().isoformat(),
            )
            if collapse_key in seen_single_member_days:
                continue
            seen_single_member_days.add(collapse_key)

        collapsed.append(row)
        if len(collapsed) >= limit:
            break

    return collapsed


def render_recent_tickets(rows):
    if not rows:
        return (
            '<div class="ckt-ticket">'
            '<div class="ckt-meta">Archive note</div>'
            "<strong>No completed calls yet</strong>"
            "<div>Completed Chekicha sessions will appear here.</div>"
            "</div>"
        )

    parts = []
    for row in rows:
        dt = pd.to_datetime(row["start_time"])
        parts.append(
            (
                '<div class="ckt-ticket">'
                f'<div class="ckt-meta">{safe_text(format_event_date(dt))}</div>'
                f'<strong>{safe_text(row.get("nickname", "Unknown member"))}</strong>'
                f'<div>{safe_text(row.get("event_name", "Untitled event"))}</div>'
                "</div>"
            )
        )
    return "".join(parts)


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
    page_title="Overview · Chekicha Timeline",
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
members_res = supabase.table("members").select("id, status", count="exact").execute()

event_rows = events_res.data or []
total_events = events_res.count or 0
total_members = members_res.count or 0
total_pending = 0
completed_rows = []

for row in event_rows:
    slot_mode = row.get("slot_mode") or 1
    member_a_id = row.get("member_id_a")
    member_b_id = row.get("member_id_b")
    member_a = relation_to_member(row.get("member_a"))
    member_b = relation_to_member(row.get("member_b"))

    if not member_a_id:
        total_pending += 1
    else:
        completed_rows.append(
            {
                "event_name": row.get("event_name"),
                "event_type": row.get("event_type"),
                "start_time": row.get("start_time"),
                "nickname": member_a.get("nickname", "Unknown member"),
                "avatar_url": member_a.get("avatar_url"),
                "generasi": member_a.get("generasi"),
            }
        )

    if slot_mode == 2:
        if not member_b_id:
            total_pending += 1
        else:
            completed_rows.append(
                {
                    "event_name": row.get("event_name"),
                    "event_type": row.get("event_type"),
                    "start_time": row.get("start_time"),
                    "nickname": member_b.get("nickname", "Unknown member"),
                    "avatar_url": member_b.get("avatar_url"),
                    "generasi": member_b.get("generasi"),
                }
            )

resolved_calls = len(completed_rows)
total_slots = total_pending + resolved_calls
completion_rate = round((resolved_calls / total_slots) * 100) if total_slots else 0
type_counts = pd.Series([r["event_type"] for r in event_rows]).value_counts()
top_event_type = type_counts.index[0] if not type_counts.empty else "No events yet"
top_event_count = int(type_counts.iloc[0]) if not type_counts.empty else 0
roulette_member_rows = [row for row in completed_rows if row.get("event_type") == "Roulette"]
roulette_member_counts = pd.Series([row["nickname"] for row in roulette_member_rows]).value_counts()
roulette_member_avatars = {}
roulette_member_generations = {}
for row in roulette_member_rows:
    roulette_member_avatars.setdefault(row["nickname"], row.get("avatar_url"))
    roulette_member_generations.setdefault(row["nickname"], row.get("generasi"))
top_roulette_rows = [
    {
        "nickname": name,
        "count": int(count),
        "avatar_url": roulette_member_avatars.get(name),
        "generasi": roulette_member_generations.get(name),
    }
    for name, count in roulette_member_counts.head(8).items()
]
latest_archive = max((pd.to_datetime(row["start_time"]) for row in event_rows), default=None)
latest_archive_copy = format_event_date(latest_archive) if latest_archive is not None else "No archive dates yet"
recent_completed_rows = collapse_recent_calls(completed_rows, limit=5)

hydrate_admin_access()
render_navbar("overview", total_pending)
st.markdown('<div class="ct-content ct-archive">', unsafe_allow_html=True)

waiting_copy = (
    f"{total_pending} draw{'s' if total_pending != 1 else ''} still waiting"
    if total_pending
    else "No roulette draws waiting"
)

top_member = top_roulette_rows[0] if top_roulette_rows else None
top_member_name = top_member["nickname"] if top_member else "No winner yet"
top_member_subcopy = (
    f"Seen in {top_member['count']} completed roulette slot{'s' if top_member['count'] != 1 else ''}"
    if top_member
    else "Winners will appear here after results are assigned"
)
archive_help = (
    "Start with the open draws. They stay at the top until every slot has a winner."
    if total_pending
    else "Everything is assigned right now, so you can move straight to the latest results below."
)

st.markdown(
    f"""
    <section class="ckt-hero ckt-overview-hero">
      <div class="ckt-status-strip ckt-surface">
        <div class="ckt-status-cell">
          <div class="ckt-meta">Still open</div>
          <strong class="ckt-status-value {'is-hot' if total_pending else ''}">{safe_text(waiting_copy)}</strong>
          <div class="ckt-status-subline">Check these first before looking at older results.</div>
        </div>
        <div class="ckt-status-cell">
          <div class="ckt-meta">Latest event</div>
          <strong class="ckt-status-value">{safe_text(latest_archive_copy)}</strong>
          <div class="ckt-status-subline">The newest event currently saved in the archive.</div>
        </div>
        <div class="ckt-status-cell">
          <div class="ckt-meta">Most seen member</div>
          <strong class="ckt-status-value">{safe_text(top_member_name)}</strong>
          <div class="ckt-status-subline">{safe_text(top_member_subcopy)}</div>
        </div>
        <div class="ckt-status-cell">
          <div class="ckt-meta">Most common format</div>
          <strong class="ckt-status-value">{safe_text(top_event_type)}</strong>
          <div class="ckt-status-subline">{top_event_count} saved row{'s' if top_event_count != 1 else ''} use this format.</div>
        </div>
      </div>
      <div class="ckt-overview-lead">
        <div>
          <div class="ckt-kicker">JKT48 cheki tracker</div>
          <h1 class="ckt-overview-title">Start with the draws that still need a winner.</h1>
          <p class="ckt-body">Use this page as your starting point: open draws are shown first, recent winners are just below, and the rest of the archive stays easy to scan.</p>
        </div>
        <div class="ckt-overview-note">
          <div class="ckt-meta">Start here</div>
          <div class="ckt-body">{safe_text(archive_help)}</div>
        </div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

stats = [
    ("Saved events", total_events, "All event rows in the archive", "#FF6A8B"),
    ("Members listed", total_members, "Active, trainee, and graduated members", "#78E0D1"),
    ("Winners assigned", resolved_calls, "Slots that already have a member", "#F2B24A"),
    ("Archive filled", f"{completion_rate}%", "Share of all slots that already have a winner", "#C3BCDD"),
]

leaderboard_html = "".join(
    f'''
    <div class="ckt-rank-item">
      <div class="ckt-rank-position">#{index}</div>
      {render_avatar_markup(row.get("avatar_url"), row["nickname"], class_name="ckt-rank-avatar")}
      <div class="ckt-rank-copy">
        <div class="ckt-rank-name">{safe_text(row["nickname"])}</div>
          <div class="ckt-small">{safe_text(f"Gen {row['generasi']}") if row.get("generasi") else "Generation unknown"}</div>
      </div>
      <div class="ckt-rank-value">{row["count"]}</div>
    </div>
    '''
    for index, row in enumerate(top_roulette_rows, start=1)
)
if not leaderboard_html:
    leaderboard_html = '<div class="ckt-empty">No completed roulette winners yet.</div>'

type_colors = {"Roulette": "#FF6A8B", "Birthday": "#F2B24A", "Graduation": "#C3BCDD"}
bars_html = ""
for event_type, count in type_counts.items():
    pct = round(count / total_events * 100) if total_events else 0
    bars_html += f"""
    <div class="ckt-bar-row">
      <span class="ckt-bar-name">{safe_text(event_type)}</span>
      <div class="ckt-bar-track"><div class="ckt-bar-fill" style="width:{pct}%;background:{type_colors.get(event_type, '#63E6D8')}"></div></div>
      <span class="ckt-small">{count}</span>
    </div>
    """

if not bars_html:
    bars_html = '<div class="ckt-empty">Event distribution will appear once archive rows are saved.</div>'

feed_html = ""
for row in recent_completed_rows:
    nickname = row.get("nickname", "Unknown member")
    dt = pd.to_datetime(row["start_time"])
    avatar = render_avatar_markup(row.get("avatar_url"), nickname)
    feed_html += f"""
    <div class="ckt-activity-item">
      {avatar}
      <div style="min-width:0;flex:1">
        <div class="ckt-activity-top">
          <div class="ckt-activity-name">{safe_text(nickname)}</div>
          {render_event_chip(row.get("event_type", "Roulette"))}
          <span class="ckt-small ckt-activity-date">{safe_text(f"{dt.day} {dt:%b}")}</span>
        </div>
        <div class="ckt-activity-event">{safe_text(row.get("event_name", "Untitled event"))}</div>
      </div>
    </div>
    """

if not feed_html:
    feed_html = '<div class="ckt-empty">Completed calls will appear here once winners are assigned.</div>'

st.markdown(
    f"""
    <section class="ckt-grid-2 ckt-overview-grid">
      <div class="ckt-surface ckt-panel ckt-summary-panel">
        <div class="ckt-panel-head">
          <div>
            <div class="ckt-meta">Quick summary</div>
            <h2 class="ckt-panel-title">What is in the archive right now</h2>
          </div>
          <div class="ckt-panel-note">The four numbers below show how much is saved, how much is already assigned, and how complete the archive is.</div>
        </div>
        <p class="ckt-body">If you only need the big picture, start here. You can tell at a glance what still needs attention and how full the archive already is.</p>
        {render_stat_grid(stats)}
      </div>
      <div class="ckt-surface ckt-panel">
        <div class="ckt-panel-head">
          <div>
            <div class="ckt-meta">Latest winners</div>
            <h2 class="ckt-panel-title">Most recent assigned results</h2>
          </div>
          <div class="ckt-panel-note">This list helps you confirm what was assigned most recently without opening the full timeline.</div>
        </div>
        {feed_html}
      </div>
    </section>
    <section class="ckt-surface ckt-panel ckt-spotlight-panel">
      <div class="ckt-panel-head">
        <div>
          <div class="ckt-meta">Most frequent roulette winners</div>
          <h2 class="ckt-panel-title">Members that appear most often</h2>
        </div>
        <div class="ckt-panel-note">Use this to spot repeat appearances quickly when you are checking recent roulette history.</div>
      </div>
      <div class="ckt-rank-list">{leaderboard_html}</div>
    </section>
    <section class="ckt-grid-2 ckt-overview-foot">
      <div class="ckt-surface ckt-panel">
        <div class="ckt-panel-head">
          <div>
            <div class="ckt-meta">Event types</div>
            <h2 class="ckt-panel-title">How the archive is split by format</h2>
          </div>
          <div class="ckt-panel-note">Most common format: {safe_text(top_event_type)}</div>
        </div>
        {bars_html}
      </div>
      <div class="ckt-surface ckt-panel ckt-guide-panel">
        <div class="ckt-panel-head">
          <div>
            <div class="ckt-meta">What to do next</div>
            <h2 class="ckt-panel-title">Simple checks for first-time visitors</h2>
          </div>
          <div class="ckt-panel-note">These reminders explain what the numbers on this page mean and what to open next.</div>
        </div>
        <ul class="ckt-guide-list">
          <li>
            <strong>Open draws</strong>
            <span>{safe_text(waiting_copy)}</span>
          </li>
          <li>
            <strong>Filled slots</strong>
            {completion_rate}% of all saved slots already have a winner.
          </li>
          <li>
            <strong>Most common format</strong>
            {safe_text(top_event_type)} appears in {top_event_count} saved row{'s' if top_event_count != 1 else ''}.
          </li>
        </ul>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)
