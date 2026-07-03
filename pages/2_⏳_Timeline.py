import pandas as pd
import streamlit as st

from utils.styles import (
    ARCHIVE_THEME_CSS,
    DARK_THEME_CSS,
    format_event_date,
    format_event_time,
    render_avatar_markup,
    render_event_chip,
    render_navbar,
    safe_text,
)
from utils.supabase_client import get_supabase


def single_member_event(event_type: str | None) -> bool:
    return event_type in {"Birthday", "Graduation"}


def relation_to_member(value):
    if isinstance(value, list):
        return value[0] if value else None
    return value or None


def count_pending_slots(rows):
    pending = 0
    for row in rows:
        slot_mode = row.get("slot_mode") or 1
        if not row.get("member_id_a"):
            pending += 1
        if slot_mode == 2 and not row.get("member_id_b"):
            pending += 1
    return pending


def split_timeline_columns(events):
    left_column = []
    right_column = []
    for index, row in enumerate(events):
        if index % 2 == 0:
            left_column.append(row)
        else:
            right_column.append(row)
    return left_column, right_column


def group_timeline_by_month(events):
    grouped = {}
    for row in events:
        start = pd.to_datetime(row["start_time"])
        month_label = f"{start:%B %Y}"
        grouped.setdefault(month_label, []).append(row)
    return grouped


def render_member_entry(member, waiting_label: str = "Waiting for roulette"):
    if member:
        nickname = member.get("nickname") or member.get("full_name") or "Unknown member"
        return (
            f'<div class="ckt-member-pill">'
            f'{render_avatar_markup(member.get("avatar_url"), nickname)}'
            f'<span>{safe_text(nickname)}</span>'
            f"</div>"
        )
    return f'<div class="ckt-member-pill is-waiting"><span class="ckt-chip ckt-chip-waiting">{safe_text(waiting_label)}</span></div>'


def render_timeline(events):
    if not events:
        return '<div class="ckt-empty">No events match this filter.</div>'

    parts = ['<div class="ckt-timeline">']
    for row in events:
        start = pd.to_datetime(row["start_time"])
        end = pd.to_datetime(row["end_time"]) if row.get("end_time") else None

        member_a = relation_to_member(row.get("member_a"))
        member_b = relation_to_member(row.get("member_b"))
        slot_mode = row.get("slot_mode") or 1
        event_type = row.get("event_type", "Roulette")
        is_single_member = single_member_event(event_type)
        is_waiting = member_a is None or (not is_single_member and slot_mode == 2 and member_b is None)
        event_name = row.get("event_name", "Untitled event")

        if row.get("event_image_url"):
            banner = (
                f'<div class="ckt-banner"><img src="{safe_text(row["event_image_url"])}" '
                f'alt="{safe_text(event_name)} banner" loading="lazy"></div>'
            )
        else:
            banner = '<div class="ckt-banner">No banner</div>'

        if is_single_member:
            member_markup = f'<div class="ckt-member-line">{render_member_entry(member_a)}</div>'
        else:
            if slot_mode == 2:
                member_markup = (
                    '<div class="ckt-member-pair">'
                    f'{render_member_entry(member_a)}'
                    f'{render_member_entry(member_b)}'
                    "</div>"
                )
            else:
                member_markup = f'<div class="ckt-member-line">{render_member_entry(member_a)}</div>'

        parts.append(
            (
                f'<div class="ckt-surface ckt-ticket-card {"is-waiting" if is_waiting else "is-completed"}">'
                f'<div class="ckt-date-rail"><div><strong>{start.day}</strong><span>{safe_text(start.strftime("%b"))}</span></div></div>'
                f"{banner}"
                f'<div><div class="ckt-ticket-top"><div class="ckt-ticket-copy"><h3 class="ckt-ticket-name">{safe_text(event_name)}</h3>'
                f'<div class="ckt-small">{safe_text(format_event_date(start))} | {safe_text(format_event_time(start, end))}</div>'
                f'</div>{render_event_chip(event_type)}</div>'
                f"{member_markup}</div>"
                f"</div>"
            )
        )
    parts.append("</div>")
    return "".join(parts)


st.set_page_config(
    page_title="Timeline · Chekicha Timeline",
    page_icon="⏳",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(DARK_THEME_CSS + ARCHIVE_THEME_CSS, unsafe_allow_html=True)

supabase = get_supabase()
pending_rows = (
    supabase.table("chekicha").select("slot_mode, member_id_a, member_id_b").execute().data or []
)
pending_count = count_pending_slots(pending_rows)

render_navbar("timeline", pending_count)
st.markdown('<div class="ct-content ct-archive">', unsafe_allow_html=True)

raw = (
    supabase.table("chekicha")
    .select(
        "id, start_time, end_time, event_name, event_type, event_image_url, slot_mode, "
        "member_id_a, member_id_b, "
        "member_a:member_id_a(full_name, nickname, avatar_url), "
        "member_b:member_id_b(full_name, nickname, avatar_url)"
    )
    .order("start_time", desc=True)
    .execute()
    .data
    or []
)

st.markdown(
    """
    <section class="ckt-filter-row">
      <div class="ckt-filter-copy">
        <div class="ckt-kicker">Ticket Archive</div>
        <h1 class="ckt-member-title">Chronology of every draw and reveal.</h1>
        <p class="ckt-body">Waiting for roulette entries stay highlighted until every slot in the event row has a winner.</p>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

filter_widget = getattr(st, "segmented_control", None)
options = ["All", "Roulette", "Birthday", "Graduation"]
if filter_widget:
    filter_type = filter_widget("Event type", options, default="All")
else:
    filter_type = st.selectbox("Event type", options)

filtered = raw if filter_type == "All" else [row for row in raw if row.get("event_type") == filter_type]
timeline_sections = []
for month_label, month_rows in group_timeline_by_month(filtered).items():
    left_column, right_column = split_timeline_columns(month_rows)
    timeline_sections.append(
        '<section class="ckt-month-section">'
        f'<div class="ckt-month">{safe_text(month_label)}</div>'
        '<div class="ckt-timeline-columns">'
        f'<div class="ckt-timeline-col">{render_timeline(left_column)}</div>'
        f'<div class="ckt-timeline-col">{render_timeline(right_column)}</div>'
        "</div>"
        "</section>"
    )
timeline_markup = "".join(timeline_sections) if timeline_sections else '<div class="ckt-empty">No events match this filter.</div>'
st.markdown(timeline_markup, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
