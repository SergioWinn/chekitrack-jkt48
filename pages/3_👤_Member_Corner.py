import pandas as pd
import streamlit as st

from utils.admin_access import admin_nav_enabled, hydrate_admin_access
from utils.styles import (
    ARCHIVE_THEME_CSS,
    AVATAR_PALETTES,
    DARK_THEME_CSS,
    format_event_date,
    render_event_chip,
    render_navbar,
    safe_text,
)
from utils.supabase_client import get_supabase


def single_member_event(event_type: str | None) -> bool:
    return event_type in {"Birthday", "Graduation"}


def member_matches_query(member, query: str) -> bool:
    haystack = " ".join(
        [
            str(member.get("nickname") or ""),
            str(member.get("full_name") or ""),
            str(member.get("status") or ""),
            str(member.get("generasi") or ""),
        ]
    ).lower()
    return query.lower() in haystack


def count_pending_slots(rows):
    pending = 0
    for row in rows:
        slot_mode = row.get("slot_mode") or 1
        if not row.get("member_id_a"):
            pending += 1
        if slot_mode == 2 and not row.get("member_id_b"):
            pending += 1
    return pending


def build_member_archive(rows):
    history_map = {}
    for row in rows:
        member_ids = {member_id for member_id in [row.get("member_id_a"), row.get("member_id_b")] if member_id}
        for member_id in member_ids:
            history_map.setdefault(member_id, []).append(row)

    total_map = {member_id: len(member_rows) for member_id, member_rows in history_map.items()}
    limited_history_map = {member_id: member_rows[:12] for member_id, member_rows in history_map.items()}
    return limited_history_map, total_map


def render_album(history_rows, member_id):
    if not history_rows:
        return '<div class="ckt-empty">No completed calls yet. Session history will appear here.</div>'

    cards = []
    for row in history_rows:
        event_name = row.get("event_name", "Untitled event")
        event_type = row.get("event_type")
        if row.get("event_image_url"):
            thumb = (
                f'<div class="ckt-album-thumb"><img src="{safe_text(row["event_image_url"])}" '
                f'alt="{safe_text(event_name)} banner" loading="lazy"></div>'
            )
        else:
            thumb = '<div class="ckt-album-thumb ckt-banner">No banner</div>'

        date_text = format_event_date(pd.to_datetime(row["start_time"]))
        slot_chip = ""
        if not single_member_event(event_type):
            slot_label = "Slot A"
            if row.get("member_id_b") == member_id and row.get("member_id_a") != member_id:
                slot_label = "Slot B"
            elif (row.get("slot_mode") or 1) == 2 and row.get("member_id_a") == member_id and row.get("member_id_b") == member_id:
                slot_label = "Slot A+B"
            slot_chip = f'<span class="ckt-chip ckt-chip-team">{safe_text(slot_label)}</span>'

        cards.append(
            (
                '<article class="ckt-surface ckt-album-card">'
                f"{thumb}"
                f'<h3 class="ckt-ticket-name" style="font-size:1rem">{safe_text(event_name)}</h3>'
                f'<div class="ckt-small">{safe_text(date_text)}</div>'
                '<div class="ckt-meta-row" style="margin-top:10px">'
                f'{render_event_chip(event_type or "Roulette")}'
                f"{slot_chip}"
                "</div>"
                "</article>"
            )
        )
    return '<div class="ckt-album-grid">' + "".join(cards) + "</div>"


def render_member_dossier(member, history, total_cheki, palette_index: int):
    last_date = format_event_date(pd.to_datetime(history[0]["start_time"])) if history else "No completed sessions yet"
    bg, fg = AVATAR_PALETTES[palette_index % len(AVATAR_PALETTES)]
    avatar_url = member.get("avatar_url")
    if avatar_url:
        avatar_markup = (
            f'<div class="ckt-photocard-avatar"><img src="{safe_text(avatar_url)}" alt="{safe_text(member.get("nickname", ""))}" loading="lazy"></div>'
        )
    else:
        initials = "".join(word[0].upper() for word in member.get("nickname", "?").split()[:2]) or "?"
        avatar_markup = f'<div class="ckt-photocard-avatar" style="background:{bg};color:{fg}">{safe_text(initials)}</div>'

    return (
        '<section class="ckt-member-stage ckt-surface">'
        '<div class="ckt-photocard-frame">'
        f"{avatar_markup}"
        "</div>"
        "<div>"
        f'<h1 class="ckt-member-title">{safe_text(member.get("nickname", ""))}</h1>'
        f'<p class="ckt-body" style="margin-top:0">{safe_text(member.get("full_name", ""))}</p>'
        '<div class="ckt-meta-row">'
        f'<span class="ckt-chip ckt-chip-team">{safe_text(member.get("status", ""))}</span>'
        f'<span class="ckt-chip ckt-chip-team">Gen {safe_text(member.get("generasi", ""))}</span>'
        f'<span class="ckt-chip ckt-chip-completed">Total cheki {total_cheki}</span>'
        "</div>"
        f'<p class="ckt-body">Last completed session: {safe_text(last_date)}</p>'
        "</div>"
        "</section>"
        '<div class="ckt-dialog-section-title">Event history</div>'
        f'{render_album(history, member["id"])}'
    )


def render_member_card(member, palette_index: int):
    palette_bg, palette_fg = AVATAR_PALETTES[palette_index % len(AVATAR_PALETTES)]
    if member.get("avatar_url"):
        avatar_html = (
            f'<div class="ckt-member-card-ava"><img src="{safe_text(member["avatar_url"])}" '
            f'alt="{safe_text(member["nickname"])}" loading="lazy"></div>'
        )
    else:
        initials = "".join(word[0].upper() for word in member.get("nickname", "?").split()[:2]) or "?"
        avatar_html = (
            f'<div class="ckt-member-card-ava" style="background:{palette_bg};color:{palette_fg}">'
            f"{safe_text(initials)}</div>"
        )

    return (
        f'<label class="ckt-member-card-link" for="member-toggle-{safe_text(member["id"])}">'
        '<div class="ckt-member-card is-clickable">'
        f"{avatar_html}"
        f'<div class="ckt-member-card-name">{safe_text(member.get("nickname", ""))}</div>'
        f'<div class="ckt-member-card-sub">{safe_text(member.get("full_name", ""))}</div>'
        '<div class="ckt-meta-row" style="margin:10px 0 0">'
        f'<span class="ckt-chip ckt-chip-team">{safe_text(member.get("status", ""))}</span>'
        '</div>'
        '</div>'
        '</label>'
    )


def render_member_modal(member, history, total_cheki, palette_index: int):
    return (
        '<div class="ckt-member-modal">'
        f'<label class="ckt-member-modal-backdrop" for="member-toggle-{safe_text(member["id"])}"></label>'
        '<div class="ckt-member-modal-card">'
        f'<label class="ckt-member-modal-close" for="member-toggle-{safe_text(member["id"])}" aria-label="Close {safe_text(member.get("nickname", "member"))}">x</label>'
        f'{render_member_dossier(member, history, total_cheki, palette_index)}'
        '</div>'
        '</div>'
    )


def render_member_browser_item(member, history, total_cheki, palette_index: int):
    return (
        '<div class="ckt-member-browser-item">'
        f'<input id="member-toggle-{safe_text(member["id"])}" class="ckt-member-modal-toggle" type="checkbox">'
        f'{render_member_card(member, palette_index)}'
        f'{render_member_modal(member, history, total_cheki, palette_index)}'
        '</div>'
    )


st.set_page_config(
    page_title="Member Corner · Chekicha Timeline",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(DARK_THEME_CSS + ARCHIVE_THEME_CSS, unsafe_allow_html=True)

supabase = get_supabase()
pending_rows = (
    supabase.table("chekicha").select("slot_mode, member_id_a, member_id_b").execute().data or []
)
pending_count = count_pending_slots(pending_rows)

hydrate_admin_access()
render_navbar("member", pending_count, show_admin=admin_nav_enabled())
st.markdown('<div class="ct-content ct-archive">', unsafe_allow_html=True)

members_data = supabase.table("members").select("*").order("nickname").execute().data or []
if not members_data:
    st.warning("No members have been added to the archive yet.")
    st.stop()

archive_rows = (
    supabase.table("chekicha")
    .select("event_name, event_type, start_time, event_image_url, slot_mode, member_id_a, member_id_b")
    .order("start_time", desc=True)
    .execute()
    .data
    or []
)
member_history_map, total_cheki_map = build_member_archive(archive_rows)
member_order = {member["id"]: index for index, member in enumerate(members_data)}

st.markdown(
    """
    <section class="ckt-compact-intro">
      <div class="ckt-surface ckt-panel ckt-intro-panel">
        <div class="ckt-kicker">Member corner</div>
        <h1 class="ckt-member-title">Open a member profile without losing the grid.</h1>
        <p class="ckt-body">Search by nickname, full name, team, or generation, then open the profile card that matches.</p>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

status_options = ["All", "LOVE", "DREAM", "PASSION", "TRAINEE", "GRADUATED"]
search_query = st.text_input("Quick search", placeholder="Search nickname, full name, team, or generation")
status_widget = getattr(st, "segmented_control", None)
if status_widget:
    selected_status = status_widget("Team", status_options, default="All")
else:
    selected_status = st.selectbox("Team", status_options)

visible_members = [
    member for member in members_data
    if (selected_status == "All" or (member.get("status") or "").upper() == selected_status)
    and (not search_query or member_matches_query(member, search_query))
]
members_with_history = sum(1 for member in visible_members if total_cheki_map.get(member["id"], 0))

st.markdown(
    f"""
    <section class="ckt-mini-strip">
      <div class="ckt-mini-cell">
        <div class="ckt-meta">Visible members</div>
        <strong class="ckt-mini-value">{len(visible_members)}</strong>
      </div>
      <div class="ckt-mini-cell">
        <div class="ckt-meta">With archive history</div>
        <strong class="ckt-mini-value">{members_with_history}</strong>
      </div>
      <div class="ckt-mini-cell">
        <div class="ckt-meta">Current team</div>
        <strong class="ckt-mini-value">{safe_text(selected_status)}</strong>
        <div class="ckt-small">{safe_text(search_query.strip()) if search_query.strip() else 'No search keyword'}</div>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

if not visible_members:
    st.markdown('<div class="ckt-empty">No members match this team filter yet.</div>', unsafe_allow_html=True)
else:
    st.markdown(
        f'<div class="ckt-browser-meta"><div class="ckt-small">{len(visible_members)} member cards ready to open.</div>'
        '<div class="ckt-small">Click a card to inspect recent sessions without leaving the grid.</div></div>',
        unsafe_allow_html=True,
    )
    browser_markup = "".join(
        render_member_browser_item(
            member,
            member_history_map.get(member["id"], []),
            total_cheki_map.get(member["id"], 0),
            member_order[member["id"]],
        )
        for member in visible_members
    )
    st.markdown(f'<section class="ckt-member-browser-grid">{browser_markup}</section>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
